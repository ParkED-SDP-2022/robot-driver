const bcrypt = require('bcryptjs');
const db = require('../db');


module.exports = (req, res) => {
    //search if username exists
    const sql = 'SELECT * FROM user WHERE username=?';
    db(sql, req.body.username, result => {
        if (result.length >= 1) {
            return res.send({
                status: 1,
                msg: 'username already exists'
            });
        }
        const sql = 'INSERT INTO user set ?';
        req.body.password = bcrypt.hashSync(req.body.password, 10);
        const { username, email, password } = req.body;
        db(sql, {username, email, password }, result => {
            if (result.affectedRows === 1) {
                return res.send({
                    status: 0,
                    msg: "successfully registered"
                });
            }
            res.send({
                status: 1,
                msg: "failed registration"
            });
        });
    });
    // res.send(req.body);
};