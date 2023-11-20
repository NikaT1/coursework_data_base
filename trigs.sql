CREATE OR REPLACE FUNCTION check_data_for_torture() RETURNS trigger AS $$
	DECLARE
		cur_case_log_status          case_log_status;
		executor					 official_name;
		victim						 integer;
		prev_type					 integer;
    BEGIN
		cur_case_log_status = (
				select case_status from case_log where id = new.case_log_id limit 1
			);
		executor = (
				select official_name from official where id = new.executor limit 1
			);
		victim = (	
			select accused from accusation_record
			where id in (select record_id from accusation_investigative_case 
			where case_id in (select case_id from case_log where id = new.case_log_id) limit 1) limit 1
			);
        IF cur_case_log_status != 'Пыточный процесс' THEN
            RAISE EXCEPTION 'torture_log должен ссылаться на case_log пыточного процесса';
        END IF;
		IF executor != 'Фискал' THEN
            RAISE EXCEPTION 'executor должен быть фискалом';
			RETURN NULL;
        END IF;
		IF victim != NEW.victim THEN
            RAISE EXCEPTION 'значение victim указано неверно - оно не совпадает со значением обвиненного по делу';
			RETURN NULL;
        END IF;
		IF NEW.type_id != 1 THEN
			prev_type = (
				select type_id from torture_log where case_log_id = NEW.case_log_id order by type_id DESC limit 1
			);
			IF NEW.type_id - 1 = prev_type THEN
				RAISE EXCEPTION 'значение type_id указано неверно';
				RETURN NULL;
			END IF;
		END IF;
        RETURN NEW;
    END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_data_for_torture BEFORE INSERT OR UPDATE ON torture_log
    FOR EACH ROW EXECUTE FUNCTION check_data_for_torture();
	

CREATE OR REPLACE FUNCTION check_data_for_case_log() RETURNS trigger AS $$
	DECLARE
		principal					 official_name;
		step						 integer;
    BEGIN
		principal = (
				select official_name from official where id = new.principal limit 1
			);
		step = 0;
		IF (select 1 from case_log where case_log.case_id = NEW.case_id and case_log.case_status = 'Исправительная беседа') = 1 THEN
			step = 1;
		END IF;

		IF step = 1 and (select 1 from case_log where case_log.case_id = NEW.case_id and case_log.case_status = 'Пыточный процесс') = 1 THEN
			step = 2;
		END IF;

		IF step = 2 and (select 1 from case_log where case_log.case_id = NEW.case_id and case_log.case_status = 'Наказание') = 1 THEN
			step = 3;
		END IF;
			
		IF NEW.case_status = 'Пыточный процесс' and step = 1 THEN
			IF principal != 'Инквизитор'  THEN
            	RAISE EXCEPTION 'для пыточного процесса principal должен быть инквизитором';
				RETURN NULL;
			END IF;
			IF  NEW.prison_id IS NOT NULL THEN
            	RAISE EXCEPTION 'для пыточного процесса не заполняется поле prison_id';
				RETURN NULL;
			END IF;
			IF  NEW.punishment_id IS NOT NULL THEN
            	RAISE EXCEPTION 'для пыточного процесса не заполняется поле punishment_id';
				RETURN NULL;
			END IF;
			RETURN NEW;
        END IF;
		IF NEW.case_status = 'Исправительная беседа' and step = 0 THEN
			IF principal != 'Епископ'  THEN
            	RAISE EXCEPTION 'для исправительной беседы principal должен быть епископом';
				RETURN NULL;
			END IF;
			IF  NEW.prison_id IS NOT NULL THEN
            	RAISE EXCEPTION 'для исправительной беседы не заполняется поле prison_id';
				RETURN NULL;
			END IF;
			IF  NEW.punishment_id IS NOT NULL THEN
            	RAISE EXCEPTION 'для исправительной беседы не заполняется поле punishment_id';
				RETURN NULL;
			END IF;
			RETURN NEW;
        END IF;
		IF NEW.case_status = 'Наказание' and step = 2 THEN
			IF  principal != 'Светсткая власть' THEN
            	RAISE EXCEPTION 'для наказания principal должен быть светской властью';
				RETURN NULL;
			END IF; 
			IF  NEW.result IS NOT NULL THEN
            	RAISE EXCEPTION 'для наказания не заполняется поле result';
				RETURN NULL;
			END IF;
			IF  NEW.prison_id IS NULL THEN
            	RAISE EXCEPTION 'для наказания должно быть определено значение поля prison_id';
				RETURN NULL;
			END IF;
			IF  NEW.punishment_id IS NULL THEN
            	RAISE EXCEPTION 'для наказания должно быть определено значение поля punishment_id';
				RETURN NULL;
			END IF;
			RETURN NEW;
        END IF;
		
		RAISE EXCEPTION 'Выбрана неверная стадия развития дела';
        RETURN NULL;
    END;
$$ LANGUAGE plpgsql;

	
CREATE TRIGGER check_data_for_case_log BEFORE INSERT OR UPDATE ON case_log
    FOR EACH ROW EXECUTE FUNCTION check_data_for_case_log();


CREATE OR REPLACE FUNCTION check_data_for_accusation() RETURNS trigger AS $$
	DECLARE
		official					 official_name;
    BEGIN
		official = (
				select official_name from official where id = new.bishop limit 1
			);
		
		IF official != 'Епископ'  THEN
           	RAISE EXCEPTION 'получить донос может только епископ';
			RETURN NULL;
		END IF;
		
        RETURN NEW;
    END;
$$ LANGUAGE plpgsql;

	
CREATE TRIGGER check_data_for_accusation BEFORE INSERT OR UPDATE ON accusation
    FOR EACH ROW EXECUTE FUNCTION check_data_for_accusation();


CREATE OR REPLACE FUNCTION get_best_principal(cur_locality_id integer, cur_official_name official_name) RETURNS integer AS $$
	DECLARE
		principal					 integer;
	BEGIN
		 SELECT official.id INTO principal FROM official
			JOIN person on person_id = person.id
			WHERE official_name = cur_official_name and locality_id = cur_locality_id and NOT EXISTS (
				SELECT 1 FROM case_log WHERE official.id = principal)
			LIMIT 1;

		IF principal IS NOT NULL THEN
			RETURN principal;
		END IF;

		SELECT official.id INTO principal FROM official
			JOIN case_log ON official.id = case_log.principal
			JOIN person on person_id = person.id
			WHERE finish_time IS NOT NULL and official_name = cur_official_name and locality_id = cur_locality_id
			GROUP BY official.id
			HAVING COUNT(*) = (SELECT COUNT(*) FROM case_log WHERE principal = official.id)
			LIMIT 1;

		IF principal IS NOT NULL THEN
			RETURN principal;
		END IF;

		SELECT case_log.principal INTO principal FROM case_log
			JOIN official on official.id = case_log.principal
			JOIN person on person_id = person.id
			WHERE official_name = cur_official_name and locality_id = cur_locality_id
			GROUP BY case_log.principal
			ORDER BY COUNT(*) ASC
			LIMIT 1;

		RETURN principal;
END;
$$ LANGUAGE plpgsql;
		

CREATE OR REPLACE PROCEDURE start_discussion(cur_case_id integer, discription text) language plpgsql    
as $$
    DECLARE
		principal					 integer;
		locality_id					 integer;
		new_case_log_id				 integer;
    BEGIN
		locality_id = ( select church.locality_id from church 
							join inquisition_process on church_id = church.id
							join accusation on accusation.inquisition_process_id = inquisition_process.id
							join accusation_record on id_accusation = accusation.id 
							where accusation_record.id in (
								select record_id from accusation_investigative_case where case_id = cur_case_id) limit 1);
		IF locality_id IS NULL THEN
			RAISE EXCEPTION 'введенное дело не найдено';
		ELSE
			principal = get_best_principal(locality_id, 'Епископ'); 
		
			INSERT INTO case_log (case_id, case_status, principal, start_time, result, prison_id, finish_time, 
			punishment_id, description) VALUES (cur_case_id, 'Исправительная беседа', principal, CURRENT_TIMESTAMP, NULL, NULL, NULL, NULL, description)
			RETURNING id INTO new_case_log_id;
			RAISE NOTICE 'Case_log id: %', new_case_log_id;
		END IF;
	commit;
    END;$$;

CREATE OR REPLACE PROCEDURE finish_discussion(cur_case_id integer, new_result case_log_result) language plpgsql    
as $$
    DECLARE
		locality_id					 integer;
		old_case_log_id				 integer;
    BEGIN
		locality_id = ( select church.locality_id from church 
							join inquisition_process on church_id = church.id
							join accusation on accusation.inquisition_process_id = inquisition_process.id
							join accusation_record on id_accusation = accusation.id 
							where accusation_record.id in (
								select record_id from accusation_investigative_case where case_id = cur_case_id) limit 1);
		
		old_case_log_id = (select id from case_log where case_id = cur_case_id and case_status = 'Исправительная беседа' limit 1);
		IF old_case_log_id IS NULL THEN
			RAISE EXCEPTION 'беседа не была начата';
		ELSE
			UPDATE case_log SET result = new_result, finish_time = CURRENT_TIMESTAMP where id = old_case_log_id;
		END IF;
	commit;
    END;$$;