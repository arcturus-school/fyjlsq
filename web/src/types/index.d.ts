interface Res {
  code: number;
  msg: string;
}

interface UserInfoRes extends Res {
  userInfo: UserInfo;
}

interface LoginRes extends UserInfoRes {
  token: string;
}

type RegisterRes = LoginRes;

interface User {
  email: string;
  uid: number;
  avatar: string;
  user_name: string;
  roles?: string[];
}

interface UserListRes extends Res {
  users: User[];
}

interface UserInfo extends User {
  create_at: Date;
  roles: string[];
  permissions: string[];
}

interface PostData {
  content: string;
  title: string;
  cover: string;
  characters: string;
  abstract: string;
}

interface Post extends PostData {
  id?: string;
}

interface PostRes extends Res {
  id: string;
}

interface Article {
  cover: string;
  id: string;
  title: string;
  abstract: string;
  update_at: Date;
  character_count: number;
  create_at: Date;
  user: User;
}

interface ArticleDetail extends Article {
  content: string;
}

interface ArticleDetailRes extends Res {
  article: ArticleDetail;
}

interface ArticlesRes extends Res {
  articles: Article[];
}

interface ArticleRes extends Res {
  article: Article;
}

interface PersonArticle {
  cover: string;
  id: string;
  title: string;
  abstract: string;
  update_at: Date;
  character_count: number;
  create_at: Date;
}

interface PersonArticles {
  articles: PersonArticle[];
  user: User;
  page: {
    count: number;
    page_num: number;
    cur_num: number;
  };
}

interface Login {
  email: string;
  password: string;
}

interface Register {
  email: string;
  password: string;
}

interface Color {
  rgba: {
    a: number;
    b: number;
    g: number;
    r: number;
  };
  hsv: {
    h: number;
    s: number;
    v: number;
  };
  hex: string;
}
