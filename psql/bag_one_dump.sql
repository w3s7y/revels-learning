--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.1
-- Dumped by pg_dump version 9.6.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: revels; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA revels;


ALTER SCHEMA revels OWNER TO postgres;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = revels, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: bags; Type: TABLE; Schema: revels; Owner: postgres
--

CREATE TABLE bags (
    id integer NOT NULL,
    shop_id integer NOT NULL,
    total_mass real NOT NULL,
    price real NOT NULL
);


ALTER TABLE bags OWNER TO postgres;

--
-- Name: shops; Type: TABLE; Schema: revels; Owner: postgres
--

CREATE TABLE shops (
    id integer NOT NULL,
    shop_name text NOT NULL,
    address_1 text,
    address_2 text,
    address_3 text,
    postcode text NOT NULL
);


ALTER TABLE shops OWNER TO postgres;

--
-- Name: bags_detail; Type: VIEW; Schema: revels; Owner: postgres
--

CREATE VIEW bags_detail AS
 SELECT bags.id,
    bags.total_mass,
    bags.price,
    shops.shop_name,
    shops.address_1,
    shops.address_2,
    shops.address_3,
    shops.postcode
   FROM (bags
     JOIN shops ON ((bags.shop_id = shops.id)));


ALTER TABLE bags_detail OWNER TO postgres;

--
-- Name: bags_id_seq; Type: SEQUENCE; Schema: revels; Owner: postgres
--

CREATE SEQUENCE bags_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE bags_id_seq OWNER TO postgres;

--
-- Name: bags_id_seq; Type: SEQUENCE OWNED BY; Schema: revels; Owner: postgres
--

ALTER SEQUENCE bags_id_seq OWNED BY bags.id;


--
-- Name: data; Type: TABLE; Schema: revels; Owner: postgres
--

CREATE TABLE data (
    id integer NOT NULL,
    bag_id integer NOT NULL,
    type_id integer NOT NULL,
    mass real NOT NULL,
    density real NOT NULL,
    height real NOT NULL,
    width real NOT NULL,
    depth real NOT NULL
);


ALTER TABLE data OWNER TO postgres;

--
-- Name: data_id_seq; Type: SEQUENCE; Schema: revels; Owner: postgres
--

CREATE SEQUENCE data_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE data_id_seq OWNER TO postgres;

--
-- Name: data_id_seq; Type: SEQUENCE OWNED BY; Schema: revels; Owner: postgres
--

ALTER SEQUENCE data_id_seq OWNED BY data.id;


--
-- Name: types; Type: TABLE; Schema: revels; Owner: postgres
--

CREATE TABLE types (
    id integer NOT NULL,
    type_name text NOT NULL
);


ALTER TABLE types OWNER TO postgres;

--
-- Name: revels_detail; Type: VIEW; Schema: revels; Owner: postgres
--

CREATE VIEW revels_detail AS
 SELECT data.id AS data_id,
    bags.id AS bag_id,
    shops.id AS shop_id,
    types.type_name,
    data.type_id,
    data.mass,
    data.density,
    data.height,
    data.width,
    data.depth
   FROM (((data
     JOIN bags ON ((data.bag_id = bags.id)))
     JOIN shops ON ((shops.id = bags.id)))
     JOIN types ON ((types.id = data.type_id)));


ALTER TABLE revels_detail OWNER TO postgres;

--
-- Name: shops_id_seq; Type: SEQUENCE; Schema: revels; Owner: postgres
--

CREATE SEQUENCE shops_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE shops_id_seq OWNER TO postgres;

--
-- Name: shops_id_seq; Type: SEQUENCE OWNED BY; Schema: revels; Owner: postgres
--

ALTER SEQUENCE shops_id_seq OWNED BY shops.id;


--
-- Name: types_id_seq; Type: SEQUENCE; Schema: revels; Owner: postgres
--

CREATE SEQUENCE types_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE types_id_seq OWNER TO postgres;

--
-- Name: types_id_seq; Type: SEQUENCE OWNED BY; Schema: revels; Owner: postgres
--

ALTER SEQUENCE types_id_seq OWNED BY types.id;


--
-- Name: bags id; Type: DEFAULT; Schema: revels; Owner: postgres
--

ALTER TABLE ONLY bags ALTER COLUMN id SET DEFAULT nextval('bags_id_seq'::regclass);


--
-- Name: data id; Type: DEFAULT; Schema: revels; Owner: postgres
--

ALTER TABLE ONLY data ALTER COLUMN id SET DEFAULT nextval('data_id_seq'::regclass);


--
-- Name: shops id; Type: DEFAULT; Schema: revels; Owner: postgres
--

ALTER TABLE ONLY shops ALTER COLUMN id SET DEFAULT nextval('shops_id_seq'::regclass);


--
-- Name: types id; Type: DEFAULT; Schema: revels; Owner: postgres
--

ALTER TABLE ONLY types ALTER COLUMN id SET DEFAULT nextval('types_id_seq'::regclass);


--
-- Data for Name: bags; Type: TABLE DATA; Schema: revels; Owner: postgres
--

COPY bags (id, shop_id, total_mass, price) FROM stdin;
1	2	112	1
\.


--
-- Name: bags_id_seq; Type: SEQUENCE SET; Schema: revels; Owner: postgres
--

SELECT pg_catalog.setval('bags_id_seq', 1, true);


--
-- Data for Name: data; Type: TABLE DATA; Schema: revels; Owner: postgres
--

COPY data (id, bag_id, type_id, mass, density, height, width, depth) FROM stdin;
1	1	5	2.56999993	1.24000001	17.9799995	18.5799999	18.7399998
2	1	2	2.1099999	1.25999999	12.7600002	16.2800007	14.5
3	1	6	2.06999993	1.22000003	8.18000031	19.2999992	19.3400002
4	1	3	3.31999993	1.24000001	17	16.8799992	16.7399998
5	1	5	2.20000005	0.5	17.9200001	19.1200008	19.3400002
6	1	3	3.18000007	1.25	16.6800003	16.1800003	16.4200001
7	1	6	2.13000011	1.24000001	8.30000019	19.6599998	19.4200001
8	1	6	2.0999999	1.22000003	8.10000038	19.3799992	19.5599995
9	1	2	2.42000008	1.26999998	13.8400002	16.8199997	15.0799999
10	1	4	3.07999992	1.22000003	15.7600002	16.8600006	15.8999996
11	1	2	2.55999994	1.27999997	13.2799997	17.2600002	15.8000002
12	1	1	1.54999995	1.22000003	11.1800003	14.4399996	12.8999996
13	1	6	2.05999994	1.23000002	8.10999966	19.4200001	18.4599991
14	1	6	2.08999991	1.22000003	8.10000038	19.2199993	19.1599998
15	1	1	1.46000004	1.17999995	9.43999958	18.1000004	12.1800003
16	1	3	3.02999997	1.22000003	16.3799992	16.1599998	16.1800003
17	1	4	2.8900001	1.22000003	14.7200003	16.3799992	16.3600006
18	1	4	2.8900001	1.22000003	15.0799999	16.6800003	16.1599998
19	1	4	2.58999991	1.23000002	14.8000002	15	15.3000002
20	1	2	2.0999999	1.28999996	12.8999996	16.4799995	14.1000004
21	1	2	2.18000007	1.25	13	16.8199997	14.9200001
22	1	2	1.92999995	1.25999999	12.1599998	16.3600006	14.4200001
23	1	5	2.20000005	0.5	17.6399994	19.0599995	18.6000004
24	1	5	2.19000006	0.5	18.0400009	19.1399994	18.6000004
25	1	5	2.43000007	0.5	17.7999992	19.3199997	18.2999992
26	1	6	2.07999992	1.27999997	8.11999989	19.1000004	19.1800003
27	1	6	2.13000011	1.24000001	8.14000034	19.3999996	19.1599998
28	1	6	2.04999995	1.21000004	8.14000034	19.0200005	19.6399994
29	1	6	2.1099999	1.19000006	8.18000031	19.2000008	19.3199997
30	1	5	1.92999995	0.5	17.2999992	18.7999992	18.2399998
31	1	3	2.63000011	1.24000001	15.3400002	15.2600002	15.6000004
32	1	4	2.88000011	1.204	15.8000002	16	15.8999996
33	1	3	2.95000005	1.22000003	16.7800007	16.6399994	16.0799999
34	1	5	1.90999997	0.5	17.2600002	18.8400002	18.8400002
35	1	3	3.18000007	1.23000002	16.3600006	16.3999996	17.0799999
36	1	3	3.01999998	1.21000004	15.8999996	16.8799992	16.3799992
37	1	3	2.72000003	1.20000005	15.1000004	16.2800007	16
38	1	4	2.6500001	1.22000003	15.1000004	15.8000002	15.4799995
39	1	4	2.9000001	1.21000004	15.46	16.4200001	16.0200005
40	1	2	2.25	1.26999998	12.7399998	17.5599995	14.7799997
41	1	2	2.07999992	1.25	12.8400002	16	14.5600004
42	1	1	2.07999992	1.23000002	11.5799999	17.8600006	14.7200003
43	1	1	1.25999999	1.16999996	7.94000006	16.5799999	13.4200001
44	1	1	1.55999994	1.14999998	9.92000008	18.2999992	12.6800003
45	1	1	2.02999997	1.21000004	10	20	14
46	1	1	1.78999996	1.21000004	10.8000002	17.7199993	13.3199997
47	1	1	1.60000002	1.19000006	10.6000004	17.0799999	13
48	1	1	1.51999998	1.17999995	9.52000046	18.3999996	12.4399996
49	1	1	1.46000004	1.19000006	8.64000034	18	12.8999996
50	1	2	2.07999992	1.25	12.2799997	17	13.7399998
\.


--
-- Name: data_id_seq; Type: SEQUENCE SET; Schema: revels; Owner: postgres
--

SELECT pg_catalog.setval('data_id_seq', 50, true);


--
-- Data for Name: shops; Type: TABLE DATA; Schema: revels; Owner: postgres
--

COPY shops (id, shop_name, address_1, address_2, address_3, postcode) FROM stdin;
1	Tesco Express	Saffron Square	Wellsley Road	Croydon	CR9 2BY
2	Spar	93 - 95 High Street	Porthmadog	Wales	LL49 9EU
3	Riverside Shopping Centre	Pride Hill Centre	Shrewsbury	Shropshire	SY1 1BU
\.


--
-- Name: shops_id_seq; Type: SEQUENCE SET; Schema: revels; Owner: postgres
--

SELECT pg_catalog.setval('shops_id_seq', 3, true);


--
-- Data for Name: types; Type: TABLE DATA; Schema: revels; Owner: postgres
--

COPY types (id, type_name) FROM stdin;
1	Raisin
2	Toffee
3	Orange
4	Coffee
5	Malteser
6	Galaxy Counter
\.


--
-- Name: types_id_seq; Type: SEQUENCE SET; Schema: revels; Owner: postgres
--

SELECT pg_catalog.setval('types_id_seq', 6, true);


--
-- Name: bags bags_pkey; Type: CONSTRAINT; Schema: revels; Owner: postgres
--

ALTER TABLE ONLY bags
    ADD CONSTRAINT bags_pkey PRIMARY KEY (id);


--
-- Name: data data_pkey; Type: CONSTRAINT; Schema: revels; Owner: postgres
--

ALTER TABLE ONLY data
    ADD CONSTRAINT data_pkey PRIMARY KEY (id);


--
-- Name: shops shops_pkey; Type: CONSTRAINT; Schema: revels; Owner: postgres
--

ALTER TABLE ONLY shops
    ADD CONSTRAINT shops_pkey PRIMARY KEY (id);


--
-- Name: types types_pkey; Type: CONSTRAINT; Schema: revels; Owner: postgres
--

ALTER TABLE ONLY types
    ADD CONSTRAINT types_pkey PRIMARY KEY (id);


--
-- Name: bags bags_shop_id_fkey; Type: FK CONSTRAINT; Schema: revels; Owner: postgres
--

ALTER TABLE ONLY bags
    ADD CONSTRAINT bags_shop_id_fkey FOREIGN KEY (shop_id) REFERENCES shops(id);


--
-- Name: data data_bag_id_fkey; Type: FK CONSTRAINT; Schema: revels; Owner: postgres
--

ALTER TABLE ONLY data
    ADD CONSTRAINT data_bag_id_fkey FOREIGN KEY (bag_id) REFERENCES bags(id);


--
-- Name: data data_type_id_fkey; Type: FK CONSTRAINT; Schema: revels; Owner: postgres
--

ALTER TABLE ONLY data
    ADD CONSTRAINT data_type_id_fkey FOREIGN KEY (type_id) REFERENCES types(id);


--
-- Name: revels; Type: ACL; Schema: -; Owner: postgres
--

GRANT USAGE ON SCHEMA revels TO scienceuser;


--
-- Name: bags; Type: ACL; Schema: revels; Owner: postgres
--

GRANT SELECT,INSERT ON TABLE bags TO scienceuser;


--
-- Name: shops; Type: ACL; Schema: revels; Owner: postgres
--

GRANT SELECT,INSERT ON TABLE shops TO scienceuser;


--
-- Name: bags_detail; Type: ACL; Schema: revels; Owner: postgres
--

GRANT SELECT,INSERT ON TABLE bags_detail TO scienceuser;


--
-- Name: bags_id_seq; Type: ACL; Schema: revels; Owner: postgres
--

GRANT USAGE ON SEQUENCE bags_id_seq TO scienceuser;


--
-- Name: data; Type: ACL; Schema: revels; Owner: postgres
--

GRANT SELECT,INSERT ON TABLE data TO scienceuser;


--
-- Name: data_id_seq; Type: ACL; Schema: revels; Owner: postgres
--

GRANT USAGE ON SEQUENCE data_id_seq TO scienceuser;


--
-- Name: types; Type: ACL; Schema: revels; Owner: postgres
--

GRANT SELECT,INSERT ON TABLE types TO scienceuser;


--
-- Name: revels_detail; Type: ACL; Schema: revels; Owner: postgres
--

GRANT SELECT,INSERT ON TABLE revels_detail TO scienceuser;


--
-- Name: shops_id_seq; Type: ACL; Schema: revels; Owner: postgres
--

GRANT USAGE ON SEQUENCE shops_id_seq TO scienceuser;


--
-- Name: types_id_seq; Type: ACL; Schema: revels; Owner: postgres
--

GRANT USAGE ON SEQUENCE types_id_seq TO scienceuser;


--
-- PostgreSQL database dump complete
--

