import mysql from 'mysql2/promise';

export const db = mysql.createPool({
  host: 'localhost',
  user: 'root',           // default user XAMPP
  password: '',           // defaultnya kosong
  database: 'xxx', // ganti sesuai nama database
});
