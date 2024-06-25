create function f_desc_table(tbl_name character varying)
    returns TABLE(col_name text, dat_typ text, chr_max text, col_def text, is_nul text)
    language plpgsql
as
$$
begin
return query
        SELECT
               column_name::TEXT,
               data_type::TEXT,
               character_maximum_length::TEXT,
               column_default::TEXT,
               is_nullable::TEXT
               FROM information_schema.columns
        WHERE table_schema = 'public'
           AND table_name   = tbl_name;
end;
$$;

alter function f_desc_table(varchar) owner to postgres;

