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
    BEGIN
		principal = (
				select official_name from official where id = new.principal limit 1
			);
		
		IF NEW.case_status = 'Пыточный процесс' THEN
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
        END IF;
		IF NEW.case_status = 'Исправительная беседа' THEN
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
        END IF;
		IF NEW.case_status = 'Наказание' THEN
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
        END IF;
		
		
        RETURN NEW;
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