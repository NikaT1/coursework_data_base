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

CREATE OR REPLACE FUNCTION check_data_for_inquisition_process() RETURNS trigger AS $$
	DECLARE
		old_inquisition_process_id					 integer;
    BEGIN
		old_inquisition_process_id = (
				select id from inquisition_process where church_id = NEW.church_id and finish_time IS NULL
			);
		
		IF old_inquisition_process_id IS NOT NULL  THEN
           	RAISE EXCEPTION "В этой церкви в данный момент уже проводится инквизиционный процесс с id %", old_inquisition_process_id ;
			RETURN NULL;
		END IF;
		
        RETURN NEW;
    END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER check_data_for_inquisition_process BEFORE INSERT OR UPDATE ON inquisition_process
    FOR EACH ROW EXECUTE FUNCTION check_data_for_inquisition_process();


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
		

CREATE OR REPLACE FUNCTION get_best_prison(cur_locality_id integer) RETURNS integer AS $$
	DECLARE
		cur_prison_id					 integer;
	BEGIN
		 SELECT prison.id INTO cur_prison_id FROM prison
			WHERE locality_id = cur_locality_id and NOT EXISTS (
				SELECT 1 FROM case_log WHERE prison_id = prison.id)
			LIMIT 1;

		IF cur_prison_id IS NOT NULL THEN
			RETURN cur_prison_id;
		END IF;

		SELECT case_log.prison_id INTO cur_prison_id FROM case_log
			JOIN prison on prison_id = prison.id
			WHERE locality_id = cur_locality_id
			GROUP BY case_log.prison_id
			ORDER BY COUNT(*) ASC
			LIMIT 1;

		RETURN cur_prison_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION start_discussion(cur_case_id integer, discription text)  RETURNS integer   
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
			RETURN NULL;
		ELSE
			principal = get_best_principal(locality_id, 'Епископ'); 
		
			INSERT INTO case_log (case_id, case_status, principal, start_time, result, prison_id, finish_time, 
			punishment_id, description) VALUES (cur_case_id, 'Исправительная беседа', principal, CURRENT_TIMESTAMP, NULL, NULL, NULL, NULL, description)
			RETURNING id INTO new_case_log_id;
			RETURN new_case_log_id;
		END IF;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION start_torture(cur_case_id integer, discription text)  RETURNS integer   
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
			RETURN NULL;
		ELSE
			principal = get_best_principal(locality_id, 'Инквизитор'); 
		
			INSERT INTO case_log (case_id, case_status, principal, start_time, result, prison_id, finish_time, 
			punishment_id, description) VALUES (cur_case_id, 'Пыточный процесс', principal, CURRENT_TIMESTAMP, NULL, NULL, NULL, NULL, description)
			RETURNING id INTO new_case_log_id;
			RETURN new_case_log_id;
		END IF;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION finish_case_log_process(cur_case_log_id integer, cur_case_status case_log_status, new_result case_log_result)  RETURNS integer     
as $$
DECLARE
	cur_finish_time					timestamp;
BEGIN
	IF cur_case_status = "Наказание" THEN
		RAISE EXCEPTION 'Нельзя завершить наказание';
		RETURN NULL;
	END IF;
	cur_finish_time = (select finish_time from case_log where case_log.id = cur_case_log_id and case_log_status = cur_case_status; limit 1);
	IF cur_finish_time IS NULL THEN
		UPDATE case_log SET result = new_result, finish_time = CURRENT_TIMESTAMP where id = cur_case_log_id;
		RETURN cur_case_log_id;
	ELSE
		RAISE EXCEPTION 'Процесс уже окончен';
		RETURN NULL;
	END IF;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION assign_punishment(cur_case_id integer, punishment_id integer, discription text)  RETURNS integer   
as $$
    DECLARE
		prison						 integer;
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
			RAISE EXCEPTION 'Введенное дело не найдено';
			RETURN NULL;
		ELSE
			prison = get_best_prison(locality_id); 
		
			INSERT INTO case_log (case_id, case_status, principal, start_time, result, prison_id, finish_time, 
			punishment_id, description) VALUES (cur_case_id, 'Наказание', principal, CURRENT_TIMESTAMP, NULL, prison, NULL, punishment_id, description)
			RETURNING id INTO new_case_log_id;
			RETURN new_case_log_id;
		END IF;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION start_inquisition_process(church integer, bible integer)  RETURNS integer   
as $$
    DECLARE
		new_inquisition_process_id				 integer;
    BEGIN
			INSERT INTO inquisition_process (start_data, finish_data, church_id, bible_id) VALUES (GETDATE(), NULL, church, bible)
			RETURNING id INTO new_inquisition_process_id;
			RETURN new_inquisition_process_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION finish_inquisition_process(inquisition_process_id integer)  RETURNS integer   
as $$
DECLARE
	cur_finish_date					timestamp;
BEGIN
	cur_finish_date = (select finish_data from inquisition_process where inquisition_process.id = inquisition_process_id limit 1);
	IF cur_finish_date IS NULL THEN
		UPDATE inquisition_process SET finish_data = GETDATE() where id = inquisition_process_id;
		RETURN cur_case_log_id;
	ELSE
		RAISE EXCEPTION 'Процесс уже окончен';
		RETURN NULL;
	END IF;
END;
$$ LANGUAGE plpgsql;


