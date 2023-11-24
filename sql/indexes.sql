set default_text_search_config = russian;
CREATE INDEX ON commandment USING GIN(description_vector);
CREATE INDEX ON person USING btree(locality_id);
CREATE INDEX ON church USING btree(locality_id);
CREATE INDEX ON prison USING btree(locality_id);
CREATE INDEX ON locality USING btree(name);
CREATE INDEX ON person USING btree(name);