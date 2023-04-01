let express = require("express");
let app = express();
let dotenv = require("dotenv");
// let session=require("express-session");
let cookieParser = require("cookie-parser");
dotenv.config();
const Chart = require('chart.js');
const session = require('express-session');
const nocache = require("nocache");

//const path=require('path');
let port = process.env.PORT || 9100;
let mysql = require("mysql2");
var md5 = require('md5')
var sch;
var devID;
// first comment out for md5
// app.use(bodyParser.json());


//middleware
app.use(express.urlencoded({ extended: true }));
app.use(express.static(__dirname + "/public"));
app.set("view engine", "ejs");
app.use(cookieParser());
app.use(session({ secret: "soul-ltd-key", resave: false, saveUninitialized: true }))
app.use(nocache());
app.use(function (req, res, next) {
  res.header("Cache-Control", "no-cache, no-store, must-revalidate");
  res.header("Pragma", "no-cache");
  res.header("Expires", 0);
  next();
});

const connection = mysql.createPool({
  host: "souliot.mariadb.database.azure.com",
  user: "okcliot@souliot",
  password: "Siva@123",
  database: "okcldb",
});

connection.getConnection((err, connection) => {
  if (err) throw err;
  console.log('Connected to MySQL database!');
  connection.release();
});


// //all database connection information
// const connection = mysql.createConnection({
//   host: "souliot.mariadb.database.azure.com",
//   user: "okcliot@souliot",
//   password: "Siva@123",
//   database: "okcldb",
// });


// //database connection check
// connection.connect(function (err) {
//   if (err) throw err;
//   console.log("Connected!");
// });

//index page login
app.get("/", function (req, res) {
  if (req.session.user_name != null) {
    console.log(req.session.user_password)
    res.redirect("/registration")
  } else {
    res.render("index", {
      error: "", v: "", device_id: "", device_type: "", device_mq2: "",
      device_temp: "", device_hum: "",
      device_heartbeat_status: "", data: "", data1: "", data2: "", data3: "", data4: ""
    });
  }
});

app.get('/registration', function (req, res) {
  res.render("user");
  //   error: "", v: "", device_id: "", device_type: "", device_mq2: "",
  //   device_temp: "", device_hum: "",
  //   device_heartbeat_status: "", data: "", data1: "", data2: "", data3: "", data4: ""
  // });
});

// registration page
app.post("/registration", function (req, res) {
  var username = req.body.name;
  var user_password = req.body.password;

  // let scID;
  // var password=md5(user_password)   second comment out for md5
  console.log(username)
  // var sql = "SELECT username FROM user_data WHERE username = " + username.toString();
  connection.query('select school_id from keonjhar_school', (err, p) => {
    if (err) throw err;
    //here I have assigned the school_id data to the global variable that I have defined in the app.get in order to overcome the ejs error
    v = p

    connection.query("select username,user_password,privileges_user,school_id from user_data where BINARY username=?", [username], (err, x) => {
      console.log(v)
      // connection.query('select user_password from user_data where user_password=?',[md5(user_password)],(err,y)=>{ 3rd comment out
      // connection.query('select user_password from user_data where BINARY user_password=?',[md5(user_password)],(err,y)=>{

      console.log(x)
      if (x.length > 0 && x[0].username === username) {
        // console.log(results)
        console.log(x)
        // req.session.regenerate(() => {
        // req.session.loggedin = true;
        // req.session.username = username;

        // console.log(y)
        // if(y.length==0){
        //   console.log(y)
        //   res.render("index", { error: "Invalid Password" })
        // }
        if (x[0].username === username && x[0].user_password == md5(user_password) && x[0].privileges_user === "Admin") {
          console.log(x[0].user_password)
          console.log(p)
          res.render("user", { v });
        } else if (x[0].username === username && x[0].user_password == md5(user_password) && x[0].privileges_user === "User") {
          sch = x[0].school_id;
          connection.query('select device_id from okcldb.keonjhar_school_device where school_id=?', [sch], (err, dev) => {
            if (err) throw err;
            devID = dev
            console.log(dev)

          })
          req.session.username = x[0].username;
          req.session.user_password = x[0].user_password;
          req.session.privileges_user = x[0].privileges_user;
          res.redirect("school/?scID=" + x[0].school_id);


        }
        else if (x[0].username === username && x[0].user_password != md5(user_password)) {
          res.render("index", { error: "Invalid Password" })

        }

        // })

      }
      else if (x.length == 0) {

        return res.render("index", { error: "Invalid Username" });
      }


    })
  })

});




//registration page1
app.post("/d", (req, res) => {
  const { name, password, scid, eid, pu, mobile } = req.body
  console.log(req.body.name)
  console.log(req.body.password)
  console.log(req.body);
  console.log({ name, password, scid, eid, pu, mobile })

  const alertMessage = "Username already exist"
  const notification = "emp_id already exist"



  connection.query('select emp_id from user_data where emp_id=?', [eid], (err, emp) => {
    if (err) throw err
    if (emp.length > 0) {
      res.render('user', { notification, v })
    }
    else if (emp.length == 0) {
      connection.query('select username from user_data where Binary username=? ', [name], (err, x) => {
        if (x.length > 0 && x[0].username === name) {

          console.log(x)



          return res.render('user', { alertMessage, v });


        }
        else if (x.length == 0) {

          connection.query('INSERT INTO user_data SET ?', { username: name, user_password: md5(password), user_contact: mobile, privileges_user: pu, school_id: scid, emp_id: eid }, (error, y) => {
            if (error) {
              console.log(error);
            }
            else {

              // res.sendStatus(200)
              res.render('ok');
            }
          })
        }
      })

    }

  })

})

//registration page2
app.post('/d2', (req, res) => {
  const { sid, dt, idate, pdate, ds, rds } = req.body;
  connection.query('INSERT INTO okcldb.keonjhar_school_device SET ?', { school_id: sid, device_type: dt, device_status: ds, device_reset_status: rds, installation_date: idate, software_path_date: pdate }, (error, y) => {
    if (error) {
      console.log(error);
    }
    else {
      // res.sendStatus(200)
      res.render('ok');

    }
  })
})

//registration page3
app.post('/d3', (req, res) => {
  const { sclName, sclAddress, sclType, sclNumber, Inf, gps } = req.body;
  console.log({ sclName, sclAddress, sclType, sclNumber, Inf, gps })
  let pause='school_Name is already exist'
  connection.query('select school_Name from okcldb.keonjhar_school where BINARY school_Name=?',[sclName],(err,sn)=>{
    console.log(sn);
   if(sn.length==0){
  
      connection.query('INSERT INTO okcldb.keonjhar_school SET ?', { school_Name: sclName, school_address: sclAddress, school_type: sclType, school_contact: sclNumber, internet_facility: Inf, gps_cooridinate: gps }, (error, y) => {
        if (error) {
          console.log(error);
        }
        else {
          //  res.sendStatus(200)
          res.render('ok');
        }
      })}
      else if(sn[0].school_Name===sclName){
      res.render('user',{pause,v})
    }
   
 
})})




//dashboard 
app.get('/school', (req, res) => {
  let device_id = req.body.device_id;
  let device_type = req.body.device_type;
  let devicemq2 = req.body.device_mq2;
  let device_temp = req.body.device_temp;
  let device_hum = req.body.device_hum;
  let device_heartbeat_status = req.body.device_heartbeat_status;
  let scID = req.query.scID;
  sch = scID
  console.log(req.query.scID)

  // if (!req.session.loggedin) {
  //   res.redirect('/')
  // }
  // else{  

  connection.query("select * from keonjhar_school_device where school_id=?", [scID],
    function (err, result, fields) {
      connection.query('select count(*) from okcldb.keonjhar_log where log_type="Forced Entry" and log_school_id=?', [scID], (err, result1, fields) => {
        connection.query('select count(*) from okcldb.keonjhar_log where log_type="Door_Entry Granted" and log_school_id =?', [scID], (err, result2, fields) => {
          connection.query("select count(*) from okcldb.keonjhar_log where log_type ='Door_Entry Closed' and log_school_id =?", [scID], (err, result3, fields) => {
            connection.query("select count(*) from okcldb.keonjhar_log where log_type ='Door_Opened Inside' and log_school_id =?", [scID], (err, result4, fields) => {
              connection.query("select count(*) from keonjhar_log kl where substring(log_date,1,2) = SUBSTRING(curdate(),9,2) and log_type ='Door_Entry Granted' and  log_school_id=? ", [scID], (err, result5, fields) => {
                connection.query("select count(*) from keonjhar_log  where str_to_date(log_date,'%d/%m/%Y')>=curdate()and log_type ='Door_Entry Granted' and  log_school_id=?", [scID], (err, result6, fields) => {
                  connection.query("select count( *) from keonjhar_log kl where substring(log_date,4,2) = SUBSTRING(curdate(),6,2) and log_type ='Door_Entry Granted' and  log_school_id=? ", [scID], (err, result7, fields) => {
                    connection.query("SELECT count(log_time) as o ,case WHEN log_time IS NULL  THEN 0 ELSE log_time end as log_time from keonjhar_log where log_type='Door_Entry Granted' and log_school_id=? and substring(log_date,1,2) = SUBSTRING(curdate(),9,2) group by SUBSTRING(log_time,1,2)", [scID], (err, res8, fields) => {
                      connection.query("SELECT count(log_time) as close ,case WHEN log_time IS NULL  THEN 0 ELSE log_time end as log_time from keonjhar_log where log_type='Door_Entry Closed' and log_school_id=? and substring(log_date,1,2) = SUBSTRING(curdate(),9,2) group by SUBSTRING(log_time,1,2)", [scID], (err, res9, fields) => {
                        connection.query("select school_name from keonjhar_school where school_id =?", [scID], (err, res10, fields) => {
                          connection.query("select connection_status from okcldb.keonjhar_school_device where device_type ='Door' and school_id =?",[scID],  (err, result11, fields) => {
                          let on = []
                          let ti = []
                          let cl = []
                          let tl = []






                          for (var i = 0; i < res8.length; i++) {
                            on.push(res8[i].o.toString());
                            ti.push(res8[i].log_time.toString().substring(0, 2));
                          }
                          console.log(on, "  ", ti)


                          for (var i = 0; i < res9.length; i++) {
                            cl.push(res9[i].close.toString());
                            tl.push(res9[i].log_time.toString().substring(0, 2));
                          }
                          console.log(cl, "  ", tl)



                          res.render('dashboard', {
                            on, ti, cl, tl, sch, device_id: device_id, device_type: device_type, device_mq2: devicemq2,
                            device_temp: device_temp, device_hum: device_hum,
                            device_heartbeat_status: device_heartbeat_status, data: result, data1: result1, data2: result2, data3: result3, data4: result4, data5: result5, data6: result6, data7: result7, data10: res10,data11:result11
                          });
                          console.log(result5, result6, result7, res10);

                          res.end();
                        })
                      })
                      })
                    })
                  })
                })
              })
            })
          })
          // }
        })
      })
    })
})


//sensor1 school_id=dynamic
app.get('/sensor1', (req, res) => {
  let device_id = req.body.device_id;
  let device_type = req.body.device_type;
  let devicemq2 = req.body.device_mq2;
  let device_temp = req.body.device_temp;
  let device_hum = req.body.device_hum;
  let status = req.body.device_heartbeat_status;
  let device_ip = req.body.device_ip;
  let device_mac = req.body.device_mac;
  // let scID=req.query.scID
  console.log(sch)

  connection.query("select * from keonjhar_school_device where school_id=? and device_id=?", [sch, Object.values(devID[0])],

    function (err, result, fields) {
      console.log(result)
      console.log(devID[0]);
      let h = []
      let m = []
      let j = []
      let k = []
      let s = []
      let e = []

      connection.query('select device_temperature, recevied_time from okcldb.sensor_data_keonjhar where school_id=? and device_id=?', [sch, Object.values(devID[0])], (err, res1) => {
        if (err) throw err;
        //   console.log(results)

        for (var i = 0; i < res1.length; i++) {
          j.push(res1[i].device_temperature.toString());
          k.push(res1[i].recevied_time.toString().substring(0, 2));
        }
        console.log(j, "  ", k)

        // res.render('chart',{s,e,j,k,h,m})




        connection.query('select device_smoke_data, recevied_time from okcldb.sensor_data_keonjhar where school_id=?and device_id=?', [sch, Object.values(devID[0])], (err, res2) => {
          if (err) throw err;
          //   console.log(results)

          for (var i = 0; i < res2.length; i++) {
            s.push(res2[i].device_smoke_data.toString());
            e.push(res2[i].recevied_time.toString().substring(0, 2));
          }
          console.log(s, "  ", m)

          // res.render('chart',{s,e,j,k,h,m})


          connection.query('select device_humidity, recevied_time from okcldb.sensor_data_keonjhar where school_id=?and device_id=?', [sch, Object.values(devID[0])], (err, res3) => {
            if (err) throw err;
            //   console.log(results)

            for (var i = 0; i < res3.length; i++) {
              h.push(res3[i].device_humidity.toString());
              m.push(res3[i].recevied_time.toString().substring(0, 2));
            }
            // console.log(h,"  ",m)

            //   res.render('chart',{s,e,j,k,h,m})

            res.render('sensor1', {
              s, e, j, k, h, m, sch, device_id: device_id, device_type: device_type, device_mq2: devicemq2,
              device_temp: device_temp, device_hum: device_hum,
              device_heartbeat_status: status, device_ip: device_ip, device_mac: device_mac, data: result
            });
          })
        }
        )
      })
    }
  )


})


//sensor2 school_id=dynamic   
app.get('/sensor2', (req, res) => {
  let device_id = req.body.device_id;
  let device_type = req.body.device_type;
  let devicemq2 = req.body.device_mq2;
  let device_temp = req.body.device_temp;
  let device_hum = req.body.device_hum;
  let status = req.body.device_heartbeat_status;
  let device_ip = req.body.device_ip;
  let device_mac = req.body.device_mac;
  // let scID=req.query.scID
  console.log(sch)

  connection.query("select * from keonjhar_school_device where school_id=? and device_id=?", [sch, Object.values(devID[1])],
    function (err, result, fields) {
      let h = []
      let m = []
      let j = []
      let k = []
      let s = []
      let e = []

      connection.query('select device_temperature, recevied_time from okcldb.sensor_data_keonjhar where school_id=? and device_id=?', [sch, Object.values(devID[1])], (err, res1) => {
        if (err) throw err;
        //   console.log(results)

        for (var i = 0; i < res1.length; i++) {
          j.push(res1[i].device_temperature.toString());
          k.push(res1[i].recevied_time.toString().substring(0, 2));
        }
        console.log(j, "  ", k)

        // res.render('chart',{s,e,j,k,h,m})




        connection.query('select device_smoke_data, recevied_time from okcldb.sensor_data_keonjhar where school_id=?and device_id=?', [sch, Object.values(devID[1])], (err, res2) => {
          if (err) throw err;
          //   console.log(results)

          for (var i = 0; i < res2.length; i++) {
            s.push(res2[i].device_smoke_data.toString());
            e.push(res2[i].recevied_time.toString().substring(0, 2));
          }
          console.log(s, "  ", m)

          // res.render('chart',{s,e,j,k,h,m})


          connection.query('select device_humidity, recevied_time from okcldb.sensor_data_keonjhar where school_id=?and device_id=?', [sch, Object.values(devID[1])], (err, res3) => {
            if (err) throw err;
            //   console.log(results)

            for (var i = 0; i < res3.length; i++) {
              h.push(res3[i].device_humidity.toString());
              m.push(res3[i].recevied_time.toString().substring(0, 2));
            }
            // console.log(h,"  ",m)

            //   res.render('chart',{s,e,j,k,h,m})

            res.render('sensor2', {
              s, e, j, k, h, m, sch, device_id: device_id, device_type: device_type, device_mq2: devicemq2,
              device_temp: device_temp, device_hum: device_hum,
              device_heartbeat_status: status, device_ip: device_ip, device_mac: device_mac, data: result
            });
          })
        }
        )
      })
    }
  )


})

//sensor3 school_id=dynamic  
app.get('/sensor3', (req, res) => {
  let device_id = req.body.device_id;
  let device_type = req.body.device_type;
  let devicemq2 = req.body.device_mq2;
  let device_temp = req.body.device_temp;
  let device_hum = req.body.device_hum;
  let status = req.body.device_heartbeat_status;
  let device_ip = req.body.device_ip;
  let device_mac = req.body.device_mac;
  // let scID=req.query.scID
  console.log(sch)

  connection.query("select * from keonjhar_school_device where school_id=? and device_id=?", [sch, Object.values(devID[2])],
    function (err, result, fields) {
      let h = []
      let m = []
      let j = []
      let k = []
      let s = []
      let e = []

      connection.query('select device_temperature, recevied_time from okcldb.sensor_data_keonjhar where school_id=? and device_id=?', [sch, Object.values(devID[2])], (err, res1) => {
        if (err) throw err;
        //   console.log(results)

        for (var i = 0; i < res1.length; i++) {
          j.push(res1[i].device_temperature.toString());
          k.push(res1[i].recevied_time.toString().substring(0, 2));
        }
        console.log(j, "  ", k)

        // res.render('chart',{s,e,j,k,h,m})




        connection.query('select device_smoke_data, recevied_time from okcldb.sensor_data_keonjhar where school_id=?and device_id=?', [sch, Object.values(devID[2])], (err, res2) => {
          if (err) throw err;
          //   console.log(results)

          for (var i = 0; i < res2.length; i++) {
            s.push(res2[i].device_smoke_data.toString());
            e.push(res2[i].recevied_time.toString().substring(0, 2));
          }
          console.log(s, "  ", m)

          // res.render('chart',{s,e,j,k,h,m})


          connection.query('select device_humidity, recevied_time from okcldb.sensor_data_keonjhar where school_id=?and device_id=?', [sch, Object.values(devID[2])], (err, res3) => {
            if (err) throw err;
            //   console.log(results)

            for (var i = 0; i < res3.length; i++) {
              h.push(res3[i].device_humidity.toString());
              m.push(res3[i].recevied_time.toString().substring(0, 2));
            }
            // console.log(h,"  ",m)

            //   res.render('chart',{s,e,j,k,h,m})

            res.render('sensor3', {
              s, e, j, k, h, m, sch, device_id: device_id, device_type: device_type, device_mq2: devicemq2,
              device_temp: device_temp, device_hum: device_hum,
              device_heartbeat_status: status, device_ip: device_ip, device_mac: device_mac, data: result
            });
          })
        }
        )
      })
    }
  )


})
//sensor 4 school_id=dynamic
app.get('/sensor4', (req, res) => {
  let device_id = req.body.device_id;
  let device_type = req.body.device_type;
  let devicemq2 = req.body.device_mq2;
  let device_temp = req.body.device_temp;
  let device_hum = req.body.device_hum;
  let status = req.body.device_heartbeat_status;
  let device_ip = req.body.device_ip;
  let device_mac = req.body.device_mac;
  // let scID=req.query.scID
  console.log(sch)

  connection.query("select * from keonjhar_school_device where school_id=? and device_id=?", [sch, Object.values(devID[3])],
    function (err, result, fields) {
      let h = []
      let m = []
      let j = []
      let k = []
      let s = []
      let e = []

      connection.query('select device_temperature, recevied_time from okcldb.sensor_data_keonjhar where school_id=? and device_id=?', [sch, Object.values(devID[3])], (err, res1) => {
        if (err) throw err;
        //   console.log(results)

        for (var i = 0; i < res1.length; i++) {
          j.push(res1[i].device_temperature.toString());
          k.push(res1[i].recevied_time.toString().substring(0, 2));
        }
        console.log(j, "  ", k)

        // res.render('chart',{s,e,j,k,h,m})




        connection.query('select device_smoke_data, recevied_time from okcldb.sensor_data_keonjhar where school_id=?and device_id=?', [sch, Object.values(devID[3])], (err, res2) => {
          if (err) throw err;
          //   console.log(results)

          for (var i = 0; i < res2.length; i++) {
            s.push(res2[i].device_smoke_data.toString());
            e.push(res2[i].recevied_time.toString().substring(0, 2));
          }
          console.log(s, "  ", m)

          // res.render('chart',{s,e,j,k,h,m})


          connection.query('select device_humidity, recevied_time from okcldb.sensor_data_keonjhar where school_id=?and device_id=?', [sch, Object.values(devID[3])], (err, res3) => {
            if (err) throw err;
            //   console.log(results)

            for (var i = 0; i < res3.length; i++) {
              h.push(res3[i].device_humidity.toString());
              m.push(res3[i].recevied_time.toString().substring(0, 2));
            }
            // console.log(h,"  ",m)

            //   res.render('chart',{s,e,j,k,h,m})

            res.render('sensor4', {
              s, e, j, k, h, m, sch, device_id: device_id, device_type: device_type, device_mq2: devicemq2,
              device_temp: device_temp, device_hum: device_hum,
              device_heartbeat_status: status, device_ip: device_ip, device_mac: device_mac, data: result
            });
          })
        }
        )
      })
    }
  )


})

//sensor5 school_id=dynamic 
app.get('/sensor5', (req, res) => {
  let device_id = req.body.device_id;
  let device_type = req.body.device_type;
  let devicemq2 = req.body.device_mq2;
  let device_temp = req.body.device_temp;
  let device_hum = req.body.device_hum;
  let status = req.body.device_heartbeat_status;
  let device_ip = req.body.device_ip;
  let device_mac = req.body.device_mac;
  // let scID=req.query.scID
  console.log(sch)

  connection.query("select * from keonjhar_school_device where school_id=? and device_id=?", [sch, Object.values(devID[4])],
    function (err, result, fields) {
      let h = []
      let m = []
      let j = []
      let k = []
      let s = []
      let e = []

      connection.query('select device_temperature, recevied_time from okcldb.sensor_data_keonjhar where school_id=? and device_id=?', [sch, Object.values(devID[4])], (err, res1) => {
        if (err) throw err;
        //   console.log(results)

        for (var i = 0; i < res1.length; i++) {
          j.push(res1[i].device_temperature.toString());
          k.push(res1[i].recevied_time.toString().substring(0, 2));
        }
        console.log(j, "  ", k)

        // res.render('chart',{s,e,j,k,h,m})




        connection.query('select device_smoke_data, recevied_time from okcldb.sensor_data_keonjhar where school_id=?and device_id=?', [sch, Object.values(devID[4])], (err, res2) => {
          if (err) throw err;
          //   console.log(results)

          for (var i = 0; i < res2.length; i++) {
            s.push(res2[i].device_smoke_data.toString());
            e.push(res2[i].recevied_time.toString().substring(0, 2));
          }
          console.log(s, "  ", m)

          // res.render('chart',{s,e,j,k,h,m})


          connection.query('select device_humidity, recevied_time from okcldb.sensor_data_keonjhar where school_id=?and device_id=?', [sch, Object.values(devID[4])], (err, res3) => {
            if (err) throw err;
            //   console.log(results)

            for (var i = 0; i < res3.length; i++) {
              h.push(res3[i].device_humidity.toString());
              m.push(res3[i].recevied_time.toString().substring(0, 2));
            }
            // console.log(h,"  ",m)

            //   res.render('chart',{s,e,j,k,h,m})

            res.render('sensor5', {
              s, e, j, k, h, m, sch, device_id: device_id, device_type: device_type, device_mq2: devicemq2,
              device_temp: device_temp, device_hum: device_hum,
              device_heartbeat_status: status, device_ip: device_ip, device_mac: device_mac, data: result
            });
          })
        }
        )
      })
    }
  )


})
//sensor6 school_id=1   
app.get('/sensor6', (req, res) => {
  let device_id = req.body.device_id;
  let device_type = req.body.device_type;
  let devicemq2 = req.body.device_mq2;
  let device_temp = req.body.device_temp;
  let device_hum = req.body.device_hum;
  let status = req.body.device_heartbeat_status;
  let device_ip = req.body.device_ip;
  let device_mac = req.body.device_mac;
  // let scID=req.query.scID
  console.log(sch)

  connection.query("select * from keonjhar_school_device where school_id=? and device_id=?", [sch, Object.values(devID[5])],
    function (err, result, fields) {
      let h = []
      let m = []
      let j = []
      let k = []
      let s = []
      let e = []

      connection.query('select device_temperature, recevied_time from okcldb.sensor_data_keonjhar where school_id=? and device_id=?', [sch, Object.values(devID[5])], (err, res1) => {
        if (err) throw err;
        //   console.log(results)

        for (var i = 0; i < res1.length; i++) {
          j.push(res1[i].device_temperature.toString());
          k.push(res1[i].recevied_time.toString().substring(0, 2));
        }
        console.log(j, "  ", k)

        // res.render('chart',{s,e,j,k,h,m})




        connection.query('select device_smoke_data, recevied_time from okcldb.sensor_data_keonjhar where school_id=?and device_id=?', [sch, Object.values(devID[5])], (err, res2) => {
          if (err) throw err;
          //   console.log(results)

          for (var i = 0; i < res2.length; i++) {
            s.push(res2[i].device_smoke_data.toString());
            e.push(res2[i].recevied_time.toString().substring(0, 2));
          }
          console.log(s, "  ", m)

          // res.render('chart',{s,e,j,k,h,m})


          connection.query('select device_humidity, recevied_time from okcldb.sensor_data_keonjhar where school_id=?and device_id=?', [sch, Object.values(devID[5])], (err, res3) => {
            if (err) throw err;
            //   console.log(results)

            for (var i = 0; i < res3.length; i++) {
              h.push(res3[i].device_humidity.toString());
              m.push(res3[i].recevied_time.toString().substring(0, 2));
            }
            // console.log(h,"  ",m)

            //   res.render('chart',{s,e,j,k,h,m})

            res.render('sensor6', {
              s, e, j, k, h, m, sch, device_id: device_id, device_type: device_type, device_mq2: devicemq2,
              device_temp: device_temp, device_hum: device_hum,
              device_heartbeat_status: status, device_ip: device_ip, device_mac: device_mac, data: result
            });
          })
        }
        )
      })
    }
  )


})
//   app.get('/welcom',(req,res)=>{
//     let h=[]
//     let m=[]
//     let j=[]
//     let k=[]
//     let s=[]
//     let e=[]

//     connection.query('select device_temperature, recevied_time from okcldb.sensor_data_keonjhar ;',(err,results) =>{
//         if (err) throw err;
//     //   console.log(results)

//   for(var i=0;i<results.length;i++){
//       j.push(results[i].device_temperature.toString());
//       k.push(results[i].recevied_time.toString().substring(0, 2));
//   }
//     console.log(j,"  ",k)

//       // res.render('chart',{s,e,j,k,h,m})




//   connection.query('select device_smoke_data, recevied_time from okcldb.sensor_data_keonjhar ;',(err,results) =>{
//     if (err) throw err;
// //   console.log(results)

// for(var i=0;i<results.length;i++){
//   s.push(results[i].device_smoke_data.toString());
//   e.push(results[i].recevied_time.toString().substring(0, 2));
// }
// console.log(s,"  ",m)

//   // res.render('chart',{s,e,j,k,h,m})


// connection.query('select device_humidity, recevied_time from okcldb.sensor_data_keonjhar ;',(err,results) =>{
//     if (err) throw err;
// //   console.log(results)

// for(var i=0;i<results.length;i++){
//   h.push(results[i].device_humidity.toString());
//   m.push(results[i].recevied_time.toString().substring(0, 2));
// }
// console.log(h,"  ",m)

//   res.render('chart',{s,e,j,k,h,m})


// }
// )
// })  }
// )          
// }
// )    



app.get('/contact', (req, res) => {
  res.render('contact');
  res.end();
})

app.get('/logout', (req, res) => {
  console.log(req.session)

  req.session.destroy((err) => {
    if (err) {
      console.log(err);
    } else {
      res.clearCookie();
      res.redirect('/');
    }
  });

});

app.get('/soon', (req, res) => {
  res.render('soon');
})


//port connection
app.listen(port, (err) => {
  if (err) throw err;
  console.log(`server listening on ${port}`);
});