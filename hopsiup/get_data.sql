insert into users (user_id, login, password, info, upoints) values
  (1, 'andrzej1', 'a1', 'andrzej', 0),
  (2, 'andrzej2', 'a2', 'andrzej', 10);

insert into links (link_id, link, title, description, user_id, lpoints) values
  (1, 'http://github.com', 'GitHub', 'GitHub main page', 1, 20),
  (2, 'http://google.com', 'Google', 'Google search engine', 2, 30);
