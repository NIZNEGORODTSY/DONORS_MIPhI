-- public.questions определение

-- Drop table

-- DROP TABLE public.questions;

CREATE TABLE public.questions (
	id_q serial4 NOT NULL,
	uid int4 NULL,
	question text NULL,
	CONSTRAINT questions_pkey PRIMARY KEY (id_q),
	CONSTRAINT questions_uid_fkey FOREIGN KEY (uid) REFERENCES public.users(id)
);