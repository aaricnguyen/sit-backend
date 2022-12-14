/* eslint-disable no-undef */
/* eslint-disable camelcase */
import { spawn } from 'child_process';
import { difference, forEach, isEmpty } from 'lodash';
import { responseError, responseSuccess } from '../services/Response';
import logger from '../utils/logger';
import * as RedisService from '../services/RedisService';

const getDataSQL = (sqlQuery)=>{
  return new Promise((resolve, reject) => {
      con.query(sqlQuery, async (err, results = []) => {
    if (err) reject(err);
    resolve(results)
  });
  });
}

export const getUser = async (req, res) => {
  const {user_id} = req.query
  const sqlGetUser = `SELECT * FROM custConfigDB.users WHERE user_id="${user_id}"; `
  const uData = await getDataSQL(sqlGetUser)
  if (uData) {
    return res.json(
      responseSuccess({
        data: JSON.parse(JSON.stringify(uData)),
        message: 'Successfully get data.',
      }),
    );
  };
}

export const addUser = async (req, res) => {
  const {user_id, role, full_name, email, title, avatar} = req.query
  const sqlAddUser = `INSERT INTO custConfigDB.users (user_id, role, full_name, email, title, avatar) 
                      VALUES ("${user_id}", "${role}", "${full_name}", "${email}", "${title}", "${avatar}");`
  console.log('sql command', sqlAddUser)
  con.query(sqlAddUser, async (err, results) => {
    if (err) throw err;
    return res.json(
      responseSuccess({
        message: 'Successfully updated data.',
      }),
    );
  });
}

export const updateUser = async (req, res) => {
  const {user_id, role, full_name, email, title, avatar, visit_count} = req.query
  const sqlWhere = ` WHERE (user_id="${user_id}");`
  const sqlURole = role? `role="${role}" ` : `` 
  const sqlFName = full_name? `full_name="${full_name}"` : ``
  const sqlEmail = email? `email="${email}" ` : ``
  const sqlTitle = title? `title="${title}" ` : ``
  const sqlAvatar = avatar? `avatar="${avatar}" ` : ``
  const sqlVCount = visit_count? `visit_count=${visit_count}` : ``
  const sqlSet = (sqlURole + sqlFName + sqlEmail + sqlTitle + sqlAvatar + sqlVCount).replace(" ", ", ");
  const sqlUpdateUser = `UPDATE custConfigDB.users SET ` 
                        + sqlSet
                        + sqlWhere
                      
RedisService.set('totalVisit',"")

  con.query(sqlUpdateUser, async (err, results) => {
    if (err) throw err;
    return res.json(
      responseSuccess({
        message: 'Successfully updated data.',
      }),
    );
  });
}

export const getTotalVisitCount = async (req, res) => {
  const {user_id} = req.query
  const sqlTotalVisit = `SELECT SUM(visit_count) FROM custConfigDB.users;`
  const totalVisitCache = await RedisService.get('totalVisit')
  if(totalVisitCache){
    return res.json(
      responseSuccess({
        data: totalVisitCache,
        message: 'data in Cache',
      }),
    ); 
  }

  const uData = await getDataSQL(sqlTotalVisit)
  RedisService.set('totalVisit',JSON.parse(JSON.stringify(uData))[0]["SUM(visit_count)"])
  console.log(uData)
  if (uData) {
    return res.json(
      responseSuccess({
        data: JSON.parse(JSON.stringify(uData))[0]["SUM(visit_count)"],
        message: 'Successfully get data.',
      }),
    );
  };
}
