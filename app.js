const express = require('express');
const app = express();
const Joi = require('@hapi/joi');
const res = require('express/lib/response');

// application/x-www-form-urlencoded
app.use(express.urlencoded({ extended: false }));

// application/json
app.use(express.json());

app.use('/api/register', require('./routes/register'));

app.use((err, req, res, next) => {
    if (err instanceof Joi.ValidationError){
        res.send({
            status: 1,
            msg: [err.details[0].context.label, err.details[0].message]
        });
    }
    res.send({
        status: 1,
        msg: err.message || err
    });
});

app.listen(8888, () => console.log('Server running in http://localhost:8888'));