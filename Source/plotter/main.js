const input = document.querySelector('#fileInput');
const info = document.querySelector('#fileInfo');

const ctxx = document.querySelector('#xtChart');
const ctxy = document.querySelector('#ytChart');
const ctxz = document.querySelector('#ztChart');

const TIMESTEP = 0.01;

input.onchange = () => {
  info.innerHTML = input.files[0].name;
  parseFile(input.files[0], plotGraph);
}

const parseFile = (file, next) => {
  Papa.parse(file, {
    complete: function(results) {
      //console.log(results);
      let data = new Array();
      for(let i=0;i<results.data.length-1;i++){
        data.push(results.data[i].map(r => parseFloat(r)));
      }
      //console.log(data);
      next(data);
    }
  });
}

const plotGraph = data => {
  let x = [];
  let y = [];
  let z = [];

  t = 0;
  data.forEach(item => {
    x.push({x:t, y:item[0]});
    y.push({x:t, y:item[1]});
    z.push({x:t, y:item[2]});

    t += TIMESTEP;
  });

  console.log(x);
  console.log(y);
  console.log(z);

  let chartX = new Chart(ctxx, {
    type: 'scatter',
    data: {
      datasets: [
        {
          label: 'X',
          data: x,
          borderColor: '#D13E37',
          backgroundColor: 'rgba(0, 0, 0, 0)'
        },
        {
          label: 'Y',
          data: y,
          borderColor: '#67D15A',
          backgroundColor: 'rgba(0, 0, 0, 0)'
        },
        {
          label: 'Z',
          data: z,
          borderColor: '#D1C236',
          backgroundColor: 'rgba(0, 0, 0, 0)'
        }
      ]
    },
    options: {
      scales: {
        xAxes: [
          {
            type: 'linear',
            position: 'bottom',
            scaleLabel: {
              display: true,
              labelString: 't/s'
            }
          }
        ],
        yAxes: [
          {
            type: 'linear',
            scaleLabel: {
              display: true,
              labelString: 'Otklon u m po osi'
            }
          }
        ]
      }
    }
  });

}
