
CREATE OR REPLACE FUNCTION start_inquisition_process(cur_official integer, cur_church integer, cur_bible integer)  RETURNS integer   
as $$
    DECLARE
		cur_locality_id							 integer;
		new_inquisition_process_id				 integer;
		cur_person_id							 integer;
    BEGIN
			cur_locality_id = ( select church.locality_id from church where church.id = cur_church limit 1);
			cur_person_id = (select person_id from official where id = cur_official);
			UPDATE person SET locality_id = cur_locality_id where id = cur_person_id;
			INSERT INTO inquisition_process (start_data, finish_data, official_id, church_id, bible_id) VALUES (CAST (NOW() AS date), NULL, cur_official, cur_church, cur_bible)
			RETURNING id INTO new_inquisition_process_id;
			RETURN new_inquisition_process_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION finish_inquisition_process(cur_inquisition_process_id integer)  RETURNS integer   
as $$
DECLARE
	cur_finish_date					timestamp;
	case_count						integer;
	cur_accusation_id				integer;
BEGIN
	cur_finish_date = (select finish_data from inquisition_process where inquisition_process.id = cur_inquisition_process_id limit 1);
	cur_accusation_id = (select id from accusation_process where cur_inquisition_process_id = accusation_process.inquisition_process_id limit 1);
	case_count = (SELECT count(*)
			FROM investigative_case
		    WHERE investigative_case.id in (select case_id from accusation_investigative_case 
						join accusation_record on accusation_record.id = record_id 
						where id_accusation = cur_accusation_id)
					and investigative_case.closed_date is NULL);
	IF cur_finish_date IS NULL and case_count = 0 THEN
		UPDATE inquisition_process SET finish_data = CAST (NOW() AS date) where id = cur_inquisition_process_id;
		RETURN cur_inquisition_process_id;
	ELSIF case_count != 0 THEN
		RAISE EXCEPTION 'Не все дела закрыты';
		RETURN NULL;
	ELSE
		RAISE EXCEPTION 'Процесс уже окончен';
		RETURN NULL;
	END IF;
END;
$$ LANGUAGE plpgsql;




CREATE OR REPLACE FUNCTION start_accusation_process(cur_inquisition_process_id integer)  RETURNS integer   
as $$
DECLARE
	new_accusation_id				integer;
BEGIN
			INSERT INTO accusation_process (start_time, finish_time, inquisition_process_id) VALUES (CURRENT_TIMESTAMP, NULL, cur_inquisition_process_id)
			RETURNING id INTO new_accusation_id;
			RETURN new_accusation_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION finish_accusation_process(cur_accusation_id integer)  RETURNS integer   
as $$
DECLARE
	cur_finish_time					timestamp;
BEGIN
	cur_finish_time = (select finish_time from accusation_process where accusation_process.id = cur_accusation_id limit 1);
	IF cur_finish_time IS NULL THEN
		UPDATE accusation_process SET finish_time = CURRENT_TIMESTAMP where id = cur_accusation_id;
		RETURN cur_accusation_id;
	ELSE
		RAISE EXCEPTION 'Процесс уже окончен';
		RETURN NULL;
	END IF;
END;
$$ LANGUAGE plpgsql;




CREATE OR REPLACE FUNCTION add_accusation_record(cur_informer integer, cur_bishop integer, cur_accused integer, cur_violation_place varchar(255), cur_date_time timestamp, cur_description text, cur_accusation_id integer)  RETURNS integer   
as $$
DECLARE
	new_accusation_record_id				integer;
	cur_finish_time							timestamp;
BEGIN
		cur_finish_time = (select finish_time from accusation_process where accusation_process.id = cur_accusation_id limit 1);
		IF cur_finish_time IS NULL THEN	
			INSERT INTO accusation_record (informer, bishop, accused, violation_place, date_time, description, id_accusation, status) 
				VALUES (cur_informer, cur_bishop, cur_accused, cur_violation_place, cur_date_time, cur_description, cur_accusation_id, NULL)
			RETURNING id INTO new_accusation_record_id;
			RETURN new_accusation_record_id;
		ELSE
			RAISE EXCEPTION 'Процесс сбора доносов уже окончен';
			RETURN NULL;
		END IF;
END;
$$ LANGUAGE plpgsql;





CREATE OR REPLACE FUNCTION get_not_resolved_accusation_record(cur_accusation_id integer) RETURNS SETOF accusation_record
as $$
DECLARE
	cur_finish_time							timestamp;
BEGIN
		cur_finish_time = (select finish_time from accusation_process where accusation_process.id = cur_accusation_id limit 1);
		IF cur_finish_time IS NULL THEN	
			RAISE EXCEPTION 'Процесс сбора доносов еще не окончен';
		ELSE
			 RETURN QUERY EXECUTE format('SELECT * FROM accusation_record where id_accusation = %s and status is null', cur_accusation_id);	
		END IF;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION find_in_bible(phrase text, cur_bible integer) RETURNS table(cur_phrase text, cur_id integer, cur_description text) 
as $$
DECLARE
	result_row							commandment;
BEGIN
		FOR result_row IN SELECT * FROM  commandment where description ILIKE '%' || phrase || '%' and id in (select commandment_id from bible_commandment where bible_id = cur_bible) LOOP
			cur_phrase := phrase;
			cur_id := result_row.id;
			cur_description := result_row.description;
			RETURN NEXT;
		END LOOP;
		RETURN;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION read_bible(cur_bible integer) RETURNS SETOF commandment 
as $$
BEGIN
		RETURN QUERY EXECUTE format('SELECT * FROM commandment where id in (select commandment_id from bible_commandment where bible_id = %s)', cur_bible);	
END;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE FUNCTION connect_commandment_with_record(cur_commandment_id integer, cur_record_id integer) RETURNS SETOF integer 
as $$
BEGIN
	UPDATE accusation_record SET status = 'Правдивый' where id = cur_record_id;
	INSERT INTO violation (record_id, commandment_id) 
				VALUES (cur_record_id, cur_commandment_id);
	RETURN NEXT cur_commandment_id;
	RETURN NEXT cur_record_id;
END;
$$ LANGUAGE plpgsql;





CREATE OR REPLACE PROCEDURE add_record_to_case(cur_record_id integer, cur_accused integer)  
as $$
DECLARE
	cur_case							integer;
BEGIN
	cur_case = (select investigative_case.id from investigative_case where 
					EXISTS(select 1 from accusation_investigative_case
								join accusation_record on accusation_record.id = record_id
								where case_id = investigative_case.id and accusation_record.accused = cur_accused) limit 1);
	IF cur_case IS NULL THEN
		INSERT INTO investigative_case (creation_date, closed_date) 
					VALUES (CAST (NOW() AS date), NULL)
					RETURNING id INTO cur_case;
	END IF;
    INSERT INTO accusation_investigative_case (case_id, record_id) 
				VALUES (cur_case, cur_record_id); 
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION generate_cases(accusation_process integer) RETURNS SETOF investigative_case 
as $$
DECLARE
	record_id								RECORD;
	accusation_record_id					RECORD;
	new_case_id								integer;
BEGIN
	FOR record_id IN
       SELECT id
         FROM accusation_record
        WHERE status is null and id_accusation = accusation_process
    LOOP
		UPDATE accusation_record SET status = 'Ложный' where id = record_id.id;
    END LOOP;
	FOR accusation_record_id IN
       SELECT id, accused
         FROM accusation_record
        WHERE status = 'Правдивый' and id_accusation = accusation_process
    LOOP
		CALL add_record_to_case(accusation_record_id.id, accusation_record_id.accused);
    END LOOP;
	RETURN QUERY EXECUTE format('select * from investigative_case where 
								EXISTS(select 1 from accusation_investigative_case
									join accusation_record on accusation_record.id = record_id
									where case_id = investigative_case.id and id_accusation = %s)', accusation_process);
END;
$$ LANGUAGE plpgsql;






CREATE OR REPLACE PROCEDURE handle_simple_cases(cur_inquisition_process integer)
as $$
DECLARE
	cur_cases								RECORD;
	cur_accusation_id						integer;
	cur_case_count							integer;
BEGIN
	cur_accusation_id = (select id from accusation_process where inquisition_process_id = cur_inquisition_process limit 1);
	FOR cur_cases IN
       SELECT investigative_case.id as id, accusation_record.accused as accused
         FROM investigative_case
		 JOIN accusation_investigative_case on accusation_investigative_case.case_id = investigative_case.id
		 JOIN accusation_record on accusation_investigative_case.record_id = accusation_record.id
       WHERE id_accusation = cur_accusation_id and accusation_record.accused = accusation_record.informer  
	   GROUP BY investigative_case.id, accusation_record.accused
    LOOP
		cur_case_count = (select count(*) from investigative_case
							 JOIN accusation_investigative_case on accusation_investigative_case.case_id = investigative_case.id
							 JOIN accusation_record on accusation_investigative_case.record_id = accusation_record.id
							 WHERE accusation_record.accused = cur_cases.accused);
		IF cur_case_count < 2 THEN
			UPDATE investigative_case SET closed_date = CAST (NOW() AS date) WHERE investigative_case.id = cur_cases.id;
		END IF;
	END LOOP;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE PROCEDURE handle_cases_with_grave_sin (cur_inquisition_process integer)
as $$
DECLARE
	cur_cases								RECORD;
	cur_accusation_id						integer;
	cur_case_count							integer;
BEGIN
	cur_accusation_id = (select id from accusation_process where inquisition_process_id = cur_inquisition_process limit 1);
	FOR cur_cases IN
       SELECT investigative_case.id as id, accusation_record.accused as accused
         FROM investigative_case
		 JOIN accusation_investigative_case on accusation_investigative_case.case_id = investigative_case.id
		 JOIN accusation_record on accusation_investigative_case.record_id = accusation_record.id
		 JOIN violation on violation.record_id=accusation_record.id
		 JOIN commandment on commandment.id = violation.commandment_id
       WHERE id_accusation = cur_accusation_id and commandment.rank > 3
	   GROUP BY investigative_case.id, accusation_record.accused
    LOOP
		PERFORM assign_punishment(cur_cases.id, 1, 'Отправлен на наказание в связи с тяжким грехом');
		UPDATE investigative_case SET closed_date = CAST (NOW() AS date) WHERE investigative_case.id = cur_cases.id;
	END LOOP;
END;
$$ LANGUAGE plpgsql;






CREATE OR REPLACE FUNCTION get_not_resolved_cases(cur_inquisition_process integer)  RETURNS SETOF investigative_case
as $$
DECLARE
	cur_finish_time							timestamp;
	cur_accusation_id						integer;
BEGIN
		cur_accusation_id = (select id from accusation_process where inquisition_process_id = cur_inquisition_process limit 1);
		cur_finish_time = (select finish_time from accusation_process where accusation_process.id = cur_accusation_id limit 1);
		IF cur_finish_time IS NULL THEN	
			RAISE EXCEPTION 'Процесс сбора доносов еще не окончен';
		ELSE
			RETURN QUERY EXECUTE format('SELECT *
			FROM investigative_case
		    WHERE investigative_case.id in (select case_id from accusation_investigative_case 
						join accusation_record on accusation_record.id = record_id 
						where id_accusation = %s)
					and investigative_case.closed_date is NULL', cur_accusation_id);
		END IF;
END;
$$ LANGUAGE plpgsql;





CREATE OR REPLACE FUNCTION get_best_principal(cur_locality_id integer, cur_official_name official_name) RETURNS integer AS $$
	DECLARE
		cur_principal					 integer;
	BEGIN
		 SELECT official.id INTO cur_principal FROM official
			JOIN person on person_id = person.id
			WHERE official_name = cur_official_name and locality_id = cur_locality_id and NOT EXISTS (
				SELECT 1 FROM case_log WHERE case_log.principal = official.id)
			LIMIT 1;

		IF cur_principal IS NOT NULL THEN
			RETURN cur_principal;
		END IF;

		SELECT official.id INTO cur_principal FROM official
			JOIN case_log ON official.id = case_log.principal
			JOIN person on person_id = person.id
			WHERE finish_time IS NOT NULL and official_name = cur_official_name and locality_id = cur_locality_id
			GROUP BY official.id
			HAVING COUNT(*) = (SELECT COUNT(*) FROM case_log WHERE case_log.principal = official.id)
			LIMIT 1;

		IF cur_principal IS NOT NULL THEN
			RETURN cur_principal;
		END IF;

		SELECT case_log.principal INTO cur_principal FROM case_log
			JOIN official on official.id = case_log.principal
			JOIN person on person_id = person.id
			WHERE official_name = cur_official_name and locality_id = cur_locality_id
			GROUP BY case_log.principal
			ORDER BY COUNT(*) ASC
			LIMIT 1;

		RETURN cur_principal;
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





CREATE OR REPLACE FUNCTION start_discussion(cur_case_id integer)  RETURNS integer   
as $$
    DECLARE
		principal					 integer;
		locality_id					 integer;
		new_case_log_id				 integer;
    BEGIN
		locality_id = ( select church.locality_id from church 
							join inquisition_process on church_id = church.id
							join accusation_process on accusation_process.inquisition_process_id = inquisition_process.id
							join accusation_record on id_accusation = accusation_process.id 
							where accusation_record.id in (
								select record_id from accusation_investigative_case where case_id = cur_case_id) limit 1);
		IF locality_id IS NULL THEN
			RAISE EXCEPTION 'введенное дело не найдено';
			RETURN NULL;
		ELSE
			principal = get_best_principal(locality_id, 'Епископ'); 
		
			INSERT INTO case_log (case_id, case_status, principal, start_time, result, prison_id, finish_time, 
			punishment_id, description) VALUES (cur_case_id, 'Исправительная беседа', principal, CURRENT_TIMESTAMP, NULL, NULL, NULL, NULL, NULL)
			RETURNING id INTO new_case_log_id;
			RETURN new_case_log_id;
		END IF;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION start_torture(cur_case_id integer)  RETURNS integer   
as $$
    DECLARE
		principal					 integer;
		locality_id					 integer;
		new_case_log_id				 integer;
    BEGIN
		locality_id = ( select church.locality_id from church 
							join inquisition_process on church_id = church.id
							join accusation_process on accusation_process.inquisition_process_id = inquisition_process.id
							join accusation_record on id_accusation = accusation_process.id 
							where accusation_record.id in (
								select record_id from accusation_investigative_case where case_id = cur_case_id) limit 1);
		IF locality_id IS NULL THEN
			RAISE EXCEPTION 'введенное дело не найдено';
			RETURN NULL;
		ELSE
			principal = get_best_principal(locality_id, 'Инквизитор'); 
		
			INSERT INTO case_log (case_id, case_status, principal, start_time, result, prison_id, finish_time, 
			punishment_id, description) VALUES (cur_case_id, 'Пыточный процесс', principal, CURRENT_TIMESTAMP, NULL, NULL, NULL, NULL, NULL)
			RETURNING id INTO new_case_log_id;
			RETURN new_case_log_id;
		END IF;
END;
$$ LANGUAGE plpgsql;




CREATE OR REPLACE FUNCTION make_torture_step(cur_case_id integer, step integer)  RETURNS SETOF integer   
as $$
    DECLARE
		principal					 integer;
		locality_id					 integer;
		cur_case_log_id				 integer;
		cur_victim					 integer;

    BEGIN
		locality_id = ( select church.locality_id from church 
							join inquisition_process on church_id = church.id
							join accusation_process on accusation_process.inquisition_process_id = inquisition_process.id
							join accusation_record on id_accusation = accusation_process.id 
							where accusation_record.id in (
								select record_id from accusation_investigative_case where case_id = cur_case_id) limit 1);
		IF locality_id IS NULL THEN
			RAISE EXCEPTION 'Введенное дело не найдено';
		ELSE
			principal = get_best_principal(locality_id, 'Фискал'); 
			cur_victim = ( select accused from accusation_process
							join accusation_record on id_accusation = accusation_process.id 
							where accusation_record.id in (
								select record_id from accusation_investigative_case where case_id = cur_case_id) limit 1);
			cur_case_log_id = ( select case_log.id from case_log where case_id = cur_case_id and case_status = 'Пыточный процесс' );

			INSERT INTO torture_log (case_log_id, type_id, executor, victim) 
				VALUES (cur_case_log_id, step, principal, cur_victim);
			
			RETURN NEXT cur_case_id;
			RETURN NEXT step;
		END IF;
END;
$$ LANGUAGE plpgsql;




CREATE OR REPLACE FUNCTION finish_case_log_process(cur_case_log_id integer, new_result case_log_result,  cur_description text)  RETURNS integer     
as $$
DECLARE
	cur_finish_time					timestamp;
	cur_case_status					case_log_status;
	cur_case_id						integer;
BEGIN
	cur_case_status = (select case_status from case_log where case_log.id = cur_case_log_id limit 1);
	IF cur_case_status = 'Наказание' THEN
		RAISE EXCEPTION 'Нельзя завершить наказание';
		RETURN NULL;
	END IF;
	cur_finish_time = (select finish_time from case_log where case_log.id = cur_case_log_id limit 1);
	cur_case_id = (select case_id from  case_log where case_log.id = cur_case_log_id limit 1);
	IF cur_finish_time IS NULL THEN
		UPDATE case_log SET result = new_result, finish_time = CURRENT_TIMESTAMP, description = cur_description where id = cur_case_log_id;
		IF cur_case_status = 'Исправительная беседа' and new_result = 'Признание вины' THEN
			PERFORM assign_punishment(cur_case_id, 2, 'Назначена епетимья в связи с раскаянием');
			UPDATE investigative_case SET closed_date = CAST (NOW() AS date) WHERE investigative_case.id = cur_case_id;
		ELSIF cur_case_status = 'Пыточный процесс' and new_result = 'Признание вины' THEN
			PERFORM assign_punishment(cur_case_id, 3, 'Назначено аутодафе в связи с раскаянием'); 
			UPDATE investigative_case SET closed_date = CAST (NOW() AS date) WHERE investigative_case.id = cur_case_id;
		ELSIF cur_case_status = 'Пыточный процесс' and new_result = 'Отрицание вины' THEN
			PERFORM assign_punishment(cur_case_id, 1, 'Назначена казнь в связи с непризнаванием вины');
			UPDATE investigative_case SET closed_date = CAST (NOW() AS date) WHERE investigative_case.id = cur_case_id;
		END IF;
		RETURN cur_case_log_id;
	ELSE
		RAISE EXCEPTION 'Процесс уже окончен';
		RETURN NULL;
	END IF;
END;
$$ LANGUAGE plpgsql;






CREATE OR REPLACE FUNCTION assign_punishment(cur_case_id integer, cur_punishment_id integer, cur_discription text)  RETURNS integer   
as $$
    DECLARE
		prison						 integer;
		principal_id				 integer;
		locality_id					 integer;
		new_case_log_id				 integer;
    BEGIN
		locality_id = ( select church.locality_id from church 
							join inquisition_process on church_id = church.id
							join accusation_process on accusation_process.inquisition_process_id = inquisition_process.id
							join accusation_record on id_accusation = accusation_process.id 
							where accusation_record.id in (
								select record_id from accusation_investigative_case where case_id = cur_case_id) limit 1);
		IF locality_id IS NULL THEN
			RAISE EXCEPTION 'Введенное дело не найдено';
			RETURN NULL;
		ELSE
			prison = get_best_prison(locality_id); 
			principal_id = get_best_principal(locality_id, 'Светсткая власть');
			INSERT INTO case_log (case_id, case_status, principal, start_time, result, prison_id, finish_time, 
			punishment_id, description) VALUES (cur_case_id, 'Наказание', principal_id, CURRENT_TIMESTAMP, NULL, prison, NULL, cur_punishment_id, cur_discription)
			RETURNING id INTO new_case_log_id;
			RETURN new_case_log_id;
		END IF;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_cases_by_name(cur_surname text)  RETURNS SETOF investigative_case
as $$
DECLARE
	cur_persons								RECORD;
BEGIN
	FOR cur_persons IN
       SELECT person.id
         FROM person
       WHERE person.surname = cur_surname
    LOOP
		RETURN QUERY EXECUTE format('SELECT *
			FROM investigative_case
		    WHERE investigative_case.id in (select case_id from accusation_investigative_case 
						join accusation_record on accusation_record.id = record_id 
						where accused = %s)', cur_persons.id);
	END LOOP;
		
END;
$$ LANGUAGE plpgsql;

