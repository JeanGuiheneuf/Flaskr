DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS temps;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE temps (
  username TEXT PRIMARY KEY,
  présent BOOL,
  'passé-composé' BOOL,
  imparfait BOOL,
  'plus-que-parfait' BOOL,
  'passé-simple' BOOL,
  'passé-antérieur' BOOL,
  'futur-simple' BOOL,
  'futur-antérieur' BOOL,
  'conditionnel-présent' BOOL,
  'conditionnel-passé' BOOL,
  'sub_présent' BOOL,
  'sub_passé' BOOL,
  'sub_imparfait' BOOL

 );