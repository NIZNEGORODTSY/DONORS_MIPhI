-- public.users определение

-- Drop table

-- DROP TABLE public.users;

CREATE TABLE public.users (
	id serial4 NOT NULL,
	fio text NULL,
	ugroup text NULL,
	countgavr int4 NULL,
	countfmba int4 NULL,
	sumcount int4 NULL,
	lastgavr date NULL,
	lastfmba date NULL,
	contacts text NULL,
	phonenumber text NULL,
	isadmin int4 NULL,
	registry text NULL,
	tgid text NULL,
	CONSTRAINT users_pkey PRIMARY KEY (id)
);