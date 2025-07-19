-- public.upcoming_event определение

-- Drop table

-- DROP TABLE public.upcoming_event;

CREATE TABLE public.upcoming_event (
	id int4 NOT NULL,
	donplace text NOT NULL,
	dondate date NOT NULL
);