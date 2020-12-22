/*
 Navicat Premium Data Transfer

 Source Server         : localPS
 Source Server Type    : PostgreSQL
 Source Server Version : 120003
 Source Host           : localhost:5432
 Source Catalog        : fyyur
 Source Schema         : public

 Target Server Type    : PostgreSQL
 Target Server Version : 120003
 File Encoding         : 65001

 Date: 22/12/2020 23:53:14
*/


-- ----------------------------
-- Sequence structure for artists_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."artists_id_seq";
CREATE SEQUENCE "public"."artists_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;
ALTER SEQUENCE "public"."artists_id_seq" OWNER TO "mohamedziada";

-- ----------------------------
-- Sequence structure for venues_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."venues_id_seq";
CREATE SEQUENCE "public"."venues_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;
ALTER SEQUENCE "public"."venues_id_seq" OWNER TO "mohamedziada";

-- ----------------------------
-- Table structure for alembic_version
-- ----------------------------
DROP TABLE IF EXISTS "public"."alembic_version";
CREATE TABLE "public"."alembic_version" (
  "version_num" varchar(32) COLLATE "pg_catalog"."default" NOT NULL
)
;
ALTER TABLE "public"."alembic_version" OWNER TO "mohamedziada";

-- ----------------------------
-- Records of alembic_version
-- ----------------------------
BEGIN;
INSERT INTO "public"."alembic_version" VALUES ('d063fcfa29e1');
COMMIT;

-- ----------------------------
-- Table structure for artists
-- ----------------------------
DROP TABLE IF EXISTS "public"."artists";
CREATE TABLE "public"."artists" (
  "id" int4 NOT NULL DEFAULT nextval('artists_id_seq'::regclass),
  "name" varchar COLLATE "pg_catalog"."default",
  "genres" json,
  "city" varchar(120) COLLATE "pg_catalog"."default",
  "state" varchar(120) COLLATE "pg_catalog"."default",
  "phone" varchar(120) COLLATE "pg_catalog"."default",
  "website" varchar(255) COLLATE "pg_catalog"."default",
  "seeking_venue" bool,
  "seeking_description" text COLLATE "pg_catalog"."default",
  "image_link" varchar(500) COLLATE "pg_catalog"."default",
  "facebook_link" varchar(120) COLLATE "pg_catalog"."default"
)
;
ALTER TABLE "public"."artists" OWNER TO "mohamedziada";

-- ----------------------------
-- Records of artists
-- ----------------------------
BEGIN;
INSERT INTO "public"."artists" VALUES (2, 'Guns N Petals', '["Rock n Roll"]', 'San Francisco', 'CA', '326-123-5000', 'https://www.gunsnpetalsband.com', 't', 'Looking for shows to perform at in the San Francisco Bay Area!
', 'https://thispersondoesnotexist.com/image', 'https://www.facebook.com/GunsNPetals');
INSERT INTO "public"."artists" VALUES (3, 'Matt Quevedo', '["Jazz"]', 'New York', 'NY', '300-400-5000', 'https://www.gunsnpetalsband.com', 'f', 'Loyessss  the San Francisco Bay Area!
', 'https://thispersondoesnotexist.com/image', 'https://www.facebook.com/mattquevedo923251523');
INSERT INTO "public"."artists" VALUES (4, 'The Wild Sax Band', '["Jazz", "Classical"]', 'San Francisco', 'CA', '3432-325-5432', 'https://www.compeast.com', 't', 'NEWWW. San Francisco Bay Area!', 'https://thispersondoesnotexist.com/image', 'https://www.facebook.com/mattquevedo923251523');
INSERT INTO "public"."artists" VALUES (1, 'Elvis Aaron Presley', '["Rock and roll", "pop", "rockabilly", "country", "gospel", "R&B"]', 'Mississippi', 'Tupelo', '3456789', 'https://en.wikipedia.org/wiki/Elvis_Presley', 't', 'Elvis Aaron Presley (January 8, 1935 – August 16, 1977), also known simply as Elvis, was an American singer, musician and actor.', 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/99/Elvis_Presley_promoting_Jailhouse_Rock.jpg/480px-Elvis_Presley_promoting_Jailhouse_Rock.jpg', 'https://www.facebook.com');
COMMIT;

-- ----------------------------
-- Table structure for shows
-- ----------------------------
DROP TABLE IF EXISTS "public"."shows";
CREATE TABLE "public"."shows" (
  "venue_id" int4 NOT NULL,
  "artist_id" int4 NOT NULL,
  "start_time" timestamp(6) NOT NULL
)
;
ALTER TABLE "public"."shows" OWNER TO "mohamedziada";

-- ----------------------------
-- Records of shows
-- ----------------------------
BEGIN;
INSERT INTO "public"."shows" VALUES (1, 4, '2019-05-21 21:30:00');
INSERT INTO "public"."shows" VALUES (3, 1, '2019-06-15 23:00:00');
INSERT INTO "public"."shows" VALUES (3, 3, '2035-04-01 20:00:00');
INSERT INTO "public"."shows" VALUES (3, 3, '2035-04-08 20:00:00');
INSERT INTO "public"."shows" VALUES (1, 1, '2020-12-22 23:26:53');
COMMIT;

-- ----------------------------
-- Table structure for venues
-- ----------------------------
DROP TABLE IF EXISTS "public"."venues";
CREATE TABLE "public"."venues" (
  "id" int4 NOT NULL DEFAULT nextval('venues_id_seq'::regclass),
  "name" varchar COLLATE "pg_catalog"."default",
  "city" varchar(120) COLLATE "pg_catalog"."default",
  "state" varchar(120) COLLATE "pg_catalog"."default",
  "address" varchar(120) COLLATE "pg_catalog"."default",
  "phone" varchar(120) COLLATE "pg_catalog"."default",
  "image_link" varchar(500) COLLATE "pg_catalog"."default",
  "facebook_link" varchar(120) COLLATE "pg_catalog"."default",
  "genres" json,
  "website" varchar(255) COLLATE "pg_catalog"."default",
  "seeking_talent" bool,
  "seeking_description" text COLLATE "pg_catalog"."default"
)
;
ALTER TABLE "public"."venues" OWNER TO "mohamedziada";

-- ----------------------------
-- Records of venues
-- ----------------------------
BEGIN;
INSERT INTO "public"."venues" VALUES (1, 'The Musical Hop', 'San Francisco', 'CA', '1015 Folsom Street', '123-123-1234', 'https://images.unsplash.com/photo-1559076185-d25766461a17?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=2734&q=80', 'https://www.facebook.com/TheMusicalHop', '["Jazz", "Reggae", "Swing", "Classical", "Folk"]', 'https://www.themusicalhop.com', 't', 'We are on the lookout for a local artist to play every two weeks. Please call us.');
INSERT INTO "public"."venues" VALUES (3, 'Park Square Live Music & Coffee', 'San Francisco', 'CA', 'somehwrere else', '10100101010', 'https://images.unsplash.com/photo-1598628340858-201fe3c2cb7a?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=2849&q=80', 'facebook.com', '[]', NULL, 'f', NULL);
INSERT INTO "public"."venues" VALUES (2, 'The Dueling Pianos Bar', 'New York', 'NY', 'herer and here', '82498236498', 'https://images.unsplash.com/photo-1585320426283-6599b42b85ee?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=1567&q=80', 'facebook.com', '[]', NULL, 'f', NULL);
INSERT INTO "public"."venues" VALUES (4, 'sas', 'as', 'AR', 'sas', 'sa', 'ads', 'ads', '["Alternative", "Blues", "Classical"]', 'ads', 't', 'sdasd');
COMMIT;

-- ----------------------------
-- View structure for artist_view
-- ----------------------------
DROP VIEW IF EXISTS "public"."artist_view";
CREATE VIEW "public"."artist_view" AS  SELECT artists.name,
    artists.genres,
    artists.seeking_venue
   FROM artists
  WHERE (artists.seeking_venue = true);
ALTER TABLE "public"."artist_view" OWNER TO "mohamedziada";

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."artists_id_seq"
OWNED BY "public"."artists"."id";
SELECT setval('"public"."artists_id_seq"', 5, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."venues_id_seq"
OWNED BY "public"."venues"."id";
SELECT setval('"public"."venues_id_seq"', 5, true);

-- ----------------------------
-- Primary Key structure for table alembic_version
-- ----------------------------
ALTER TABLE "public"."alembic_version" ADD CONSTRAINT "alembic_version_pkc" PRIMARY KEY ("version_num");

-- ----------------------------
-- Primary Key structure for table artists
-- ----------------------------
ALTER TABLE "public"."artists" ADD CONSTRAINT "artists_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table shows
-- ----------------------------
ALTER TABLE "public"."shows" ADD CONSTRAINT "shows_pkey" PRIMARY KEY ("venue_id", "artist_id", "start_time");

-- ----------------------------
-- Foreign Keys structure for table shows
-- ----------------------------
ALTER TABLE "public"."shows" ADD CONSTRAINT "shows_artist_id_fkey" FOREIGN KEY ("artist_id") REFERENCES "public"."artists" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."shows" ADD CONSTRAINT "shows_venue_id_fkey" FOREIGN KEY ("venue_id") REFERENCES "public"."venues" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Primary Key structure for table venues
-- ----------------------------
ALTER TABLE "public"."venues" ADD CONSTRAINT "venues_pkey" PRIMARY KEY ("id");
