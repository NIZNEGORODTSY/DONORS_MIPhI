-- public.donations определение

-- Drop table

-- DROP TABLE public.donations;

CREATE TABLE public.donations (
	id serial4 NOT NULL,
	uid int4 NULL,
	donplace text NULL,
	dondate date NULL,
	CONSTRAINT donations_pkey PRIMARY KEY (id),
	CONSTRAINT donations_uid_fkey FOREIGN KEY (uid) REFERENCES public.users(id)
);