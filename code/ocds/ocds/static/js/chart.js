
// --------------------CHARTS---------------------


//area charts
var areaCharts = {
    series: [{
    name: 'SLEEP',
    type: 'area',
    data: sleep_Label
  },
  {
    name: 'AWAKE',
    type: 'line',
    data: awake_Label
  },

],
  chart: {
    type: 'line',
    height : '400px',
    foreColor: '#FFFFFF'
    
  },
  stroke: {
    curve: 'smooth'
  },
  fill: {
    type:'solid',
    opacity: [0.35, 1],
  },
  labels: range,
  markers: {
    size: 0
  },
  yaxis: [
    {
      title: {
        text: 'Y축 : SCORE',
      },
    },
    {
      opposite: true,
      title: {
        text: 'X축 : 수강시간(초)',
      },
    },
    

  ],

  
  tooltip: {
    shared: true,
    intersect: false,
    theme: "dark",
    y: {
      formatter: function (y) {
        if(typeof y !== "undefined") {
          return  y.toFixed(0) + " points";
        }
        return y;
      }
    }
  }
  };
  
  var chart_left = new ApexCharts(document.querySelector("#area-chart"), areaCharts);
  chart_left.render();
//-----------------------------------------------------------------------------------------

  // pie chart
  var pie_chart = {
    series: [numOfAwake, numOfSleep],
    // sleep 값과 awake 퍼센트값을 넣어야 한다.
    labels: ['awake','sleep'],
    chart: {
    type: 'donut',
    height: '500px',
    foreColor: '#FFFFFF'
  },

  theme: {
    monochrome: {
      enabled: true,
      color: '#255aee',
      shadeTo: 'light',
      shadeIntensity: 0.65
    }
  },
  plotOptions: {
    pie: {
      startAngle: -90,
      endAngle: 90,
      offsetY: 10
    }
  },
  grid: {
    padding: {
      bottom: -80
    }
  },
  responsive: [{
    breakpoint: 480,
    options: {
      chart: {
        width: 200
      },
      legend: {
        position: 'bottom'
      }
    }
  }]
  };

  var chart_right = new ApexCharts(document.querySelector("#pie-chart"), pie_chart);
  chart_right.render();
//----------------------------------------------------------------------



