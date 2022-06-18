const poll = async ({ fn, validate, interval, maxAttempts }) => {
  let attempts = 0;

  const executePoll = async (resolve, reject) => {
    const result = await fn();
    attempts++;

    if (validate(result)) {
      return resolve(result);
    } else if (maxAttempts && attempts === maxAttempts) {
      return reject(new Error('Exceeded max attempts'));
    } else {
      setTimeout(executePoll, interval, resolve, reject);
    }
  };

  return new Promise(executePoll);
};


// // dashboard js
// // void returns chart json
// async function getDataWrapper(){
//   const address = document.querySelector('.address').innerText;
//   const endpoint = "http://127.0.0.1:5000/csv/";
//   const newpoint = endpoint+address;
//   const value = await getData();
//   async function getData(){
//     const response = await axios.get(newpoint);
    
//     const dat = response;
//     // console.log(dat);
//     // console.log(data);
    
//     return dat;
//   }
//   return value;       
// }

// function lineChart(data){
//   let chartJson = data;
  
//   let layout = {
//     title: "<b>Wallet View</b>"
//   }
//   Plotly.newPlot("line", chartJson, layout);
// }

// function buildData(){
//   const data = getDataWrapper().then(function (data){
//     console.log(data.data);
//   });
// }

// function init(){
//   buildData();
// }
// init();