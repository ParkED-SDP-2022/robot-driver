const db = require('../db');

module.exports = (req, res) => {
    //search if username exists
    // const sql = 'SELECT * FROM user WHERE username=?';
    // db(sql, req.body.username, result => {
    //     if (result.length >= 1) {
    //         return res.send({
    //             status: 1,
    //             msg: 'username already exists'
    //         });
    //     }
    //     const sql = 'INSERT INTO user set ?';
    //     const { username, email, password } = req.body;
    //     db(sql, {username, email, password }, result => {
    //         res.send(result);
    //     });
    //     res.send({
    //         status: 0,
    //         msg: 'successfully signed up'
    //     });
    // });
    res.send(req.body);
};