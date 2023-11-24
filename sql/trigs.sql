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
			IF NEW.type_id - 1 != prev_type THEN
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
		IF (select 1 from case_log where case_log.case_id = NEW.case_id and case_log.case_status = 'Исправительная беседа' and case_log.finish_time IS NOT NULL) = 1 THEN
			step = 1;
		END IF;

		IF step = 1 and (select 1 from case_log where case_log.case_id = NEW.case_id and case_log.case_status = 'Пыточный процесс' and case_log.finish_time IS NOT NULL) = 1 THEN
			step = 2;
		END IF;

		IF step = 2 and (select 1 from case_log where case_log.case_id = NEW.case_id and case_log.case_status = 'Наказание' and case_log.finish_time IS NOT NULL) = 1 THEN
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
		IF NEW.case_status = 'Наказание' and (step = 2 or step = 0) THEN
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


CREATE OR REPLACE FUNCTION check_data_for_accusation_record() RETURNS trigger AS $$
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

	
CREATE TRIGGER check_data_for_accusation_record BEFORE INSERT OR UPDATE ON accusation_record
    FOR EACH ROW EXECUTE FUNCTION check_data_for_accusation_record();

CREATE OR REPLACE FUNCTION check_data_for_inquisition_process() RETURNS trigger AS $$
	DECLARE
		old_inquisition_process_id					 integer;
    BEGIN
		old_inquisition_process_id = (
				select id from inquisition_process where church_id = NEW.church_id and finish_data IS NULL
			);
		
		IF old_inquisition_process_id IS NOT NULL  THEN
           	RAISE EXCEPTION 'В этой церкви в данный момент уже проводится инквизиционный процесс с id %', old_inquisition_process_id ;
			RETURN NULL;
		END IF;
		
        RETURN NEW;
    END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER check_data_for_inquisition_process BEFORE INSERT ON inquisition_process
    FOR EACH ROW EXECUTE FUNCTION check_data_for_inquisition_process();

CREATE OR REPLACE FUNCTION update_content_vector() RETURNS trigger AS $$
BEGIN
  NEW.description_vector := to_tsvector('russian', NEW.description);
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER update_content_vector_trigger BEFORE INSERT OR UPDATE ON commandment
FOR EACH ROW EXECUTE FUNCTION update_content_vector();
