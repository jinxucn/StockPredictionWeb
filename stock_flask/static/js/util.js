/*
 * @Author: Jin X
 * @Date: 2019-11-27 15:58:08

 */


$(function () {
    var ctx1 = $('#chart1')
    var ctx2 = $('#chart2')
    var ctx3 = $('#chart3')
    var ctx4 = $('#chart4')
    var ctx5 = $('#chart5')
    var option = {
        scales: {
            xAxes: [{
                type: 'time',
                time: {
                    unit: 'month'
                },
                gridLines: {
                    color: "rgba(255,255,255,0.2)"
                },
            }],
            yAxes: [{
                id: 'left',
                gridLines: {
                    color: "rgba(255,255,255,0.2)"
                },
                type: 'linear',
                position: 'left'
            }, {
                id: 'right',
                type: 'linear',
                position: 'right',
            }]
        }
    };
    var chart1 = new Chart(ctx1, { type: "line", options: option })
    var chart2 = new Chart(ctx2, { type: "line", options: option })
    var chart3 = new Chart(ctx3, { type: "line", options: option })
    var chart4 = new Chart(ctx4, { type: "line", options: option })
    var chart5 = new Chart(ctx5, { type: "line", options: option })
    function plotHis(dataJson) {
        if (chart1) chart1.destroy();
        let name = dataJson['name'];
        let labels = dataJson['timestamp'];
        labels = labels.map(i => i * 1000);
        let close = dataJson['close'];
        chart1 = new Chart(ctx1, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'close',
                    data: close,
                    backgroundColor: "rgba(255,255,255,0.1)",
                    borderColor: "rgba(255,255,255,0.5)",
                }]
            },
            options: {
                scales: {
                    xAxes: [{
                        type: 'time',
                        time: {
                            unit: 'month'
                        },
                        gridLines: {
                            color: "rgba(255,255,255,0.2)"
                        },
                    }],
                    yAxes: [{
                        gridLines: {
                            color: "rgba(255,255,255,0.2)"
                        },
                    }]
                }
            },
        })
        let his = $("#historically").children().removeClass('zero')
        his[0].innerText = dataJson['high10day']
        his[1].innerText = dataJson['avg1year']
        his[2].innerText = dataJson['low1year']
        his[3].innerText = dataJson['less']
        console.log(dataJson['low1year'])
    };
    function plotIndicator(dataJson) {
        if (chart3) {
            chart3.destroy();
            chart4.destroy();
            chart5.destroy();
        }
        let labels = dataJson['timestamp'];
        labels = labels.map(i => i * 1000);
        chart3 = new Chart(ctx3, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'BBupper',
                    data: dataJson['BBupper'],
                    backgroundColor: "rgba(238,0,0,0.1)",
                    borderColor: "rgba(238,0,0,0.5)",
                    pointRadius: 1
                }, {
                    label: 'BBmiddle',
                    data: dataJson['BBmiddle'],
                    backgroundColor: "rgba(0,0,238,0.1)",
                        borderColor: "rgba(0,0,238,0.5)",
                    pointRadius: 1
                }, {
                    label: 'BBlower',
                    data: dataJson['BBlower'],
                    backgroundColor: "rgba(0,238,0,0.1)",
                    borderColor: "rgba(0,238,0,0.5)",
                    pointRadius: 1
                }]
            },
            options: {
                scales: {
                    xAxes: [{
                        type: 'time',
                        time: {
                            unit: 'day'
                        },
                        gridLines: {
                            color: "rgba(255,255,255,0.2)"
                        },
                    }],
                    yAxes: [{
                        gridLines: {
                            color: "rgba(255,255,255,0.2)"
                        },
                    }]
                }
            },
        });
        chart4 = new Chart(ctx4, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'slowD',
                    data: dataJson['slowD'],
                    backgroundColor: "rgba(238,0,0,0.1)",
                    borderColor: "rgba(238,0,0,0.5)",
                    pointRadius: 1
                }, {
                    label: 'slowK',
                    data: dataJson['slowK'],
                    backgroundColor: "rgba(0,238,0,0.1)",
                    borderColor: "rgba(0,238,0,0.5)",
                    pointRadius: 1
                }]
            },
            options: {
                scales: {
                    xAxes: [{
                        type: 'time',
                        time: {
                            unit: 'day'
                        },
                        gridLines: {
                            color: "rgba(255,255,255,0.2)"
                        },
                    }],
                    yAxes: [{
                        gridLines: {
                            color: "rgba(255,255,255,0.2)"
                        },
                    }]
                }
            },
        });
        chart5 = new Chart(ctx5, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'MACD',
                    data: dataJson['MACD'],
                    backgroundColor: "rgba(0,238,0,0.1)",
                    borderColor: "rgba(0,238,0,0.5)",
                    pointRadius: 1
                }]
            },
            options: {
                scales: {
                    xAxes: [{
                        type: 'time',
                        time: {
                            unit: 'day'
                        },
                        gridLines: {
                            color: "rgba(255,255,255,0.2)"
                        },
                    }],
                    yAxes: [{
                        gridLines: {
                            color: "rgba(255,255,255,0.2)"
                        },
                    }]
                }
            },
        });
        $('#LSTM').removeClass('zero')[0].innerText = dataJson['predict']['value']
        // console.log(dataJson['predict'])
    }
    function plotReal(dataJson) {
        if (chart2) chart2.destroy();
        let name = dataJson['name'];
        let labels = dataJson['timestamp'];
        labels = labels.map(i => i * 1000);
        let volume = dataJson['volume'];
        volume[0] = 0;
        // volume[volume.length - 1] = 0;
        let close = dataJson['close'];
        let high = dataJson['high'];
        let low = dataJson['low'];
        chart2 = new Chart(ctx2, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    type: 'line',
                    label: 'Real Time',
                    backgroundColor: "rgba(255,255,255,0.1)",
                    borderColor: "rgba(255,255,255,0.5)",
                    data: close,
                    pointRadius: 1,
                    yAxisID: 'left',
                }, {
                    type: 'line',
                    label: 'high',
                    backgroundColor: "rgba(0,205,0,0.5)",
                    borderColor: "rgba(0,205,0,0.8)",
                    data: high,
                    fill: false,
                    showLine: false,
                    pointStyle: 'cross',
                    pointRadius: 3,
                    yAxisID: 'left',
                }, {
                    type: 'line',
                    label: 'low',
                    backgroundColor: "rgba(205,0,0,0.5)",
                    borderColor: "rgba(205,0,0,0.8)",
                    data: low,
                    fill: false,
                    showLine: false,
                    pointStyle: 'line',
                    pointRadius: 3,
                    yAxisID: 'left',
                }, {
                    label: 'volume',
                    data: volume,
                    backgroundColor: "rgba(26,24,23,1)",
                    borderColor: "rgba(26,25,23,1)",
                    yAxisID: 'right',
                }]
            },
            options: {
                scales: {
                    xAxes: [{
                        type: 'time',
                        autoskip: true,
                        time: {
                            // displayFormats: {
                            //     quarter: 'll'
                            // },
                            unit: 'hour'
                        },
                        gridLines: {
                            color: "rgba(255,255,255,0.2)"
                        },
                    }],
                    yAxes: [{
                        id: 'left',
                        gridLines: {
                            color: "rgba(255,255,255,0.2)"
                        }
                    }, {
                        id: 'right',
                        gridLines: {
                            color: "rgba(25,25,25,0.2)"
                        },
                        display: false

                    }]
                }
            },
        });
        let realtime = $('#realtime').children().removeClass('zero')
        realtime[0].innerText = dataJson['high'].slice(-1)[0]
        realtime[1].innerText = dataJson['low'].slice(-1)[0]
        realtime[2].innerText = dataJson['volume'].slice(-1)[0]
        realtime[3].innerText = dataJson['open'].slice(-1)[0]
        realtime[4].innerText = dataJson['close'].slice(-1)[0]
    }
    var loopflag;
    function realTimeLoop(name) {
        console.log("getting realtime " + name);
        let url = "/stockdata?type=realtime&name=" + name;
        $.get(url, plotReal, "json");
        url = "/short?name=" + name;
        $.get(url, function (dataJson) {
            $('#Bayesian').removeClass('zero')[0].innerText = dataJson['Bayesian']['value']
            $('#SVM').removeClass('zero')[0].innerText = dataJson['SVM']['value']
        },'json')
        url = "/listsReal"
        $.get(url, function (dataJson) {
            dataJson.forEach(e => {
                $('#rt' + e['id']).text(e['price'])
            })
        }, 'json')
        loopflag = setTimeout(function () { realTimeLoop(name) }, 60000);
    }
    $.ajax({
        type: 'GET',
        timeout: 10000,
        dataType: 'json',
        url: "/stockNames",
        // data: "names"
        success: function (result) {
            let ul = $('ul.nav');
            result.forEach(e => {
                let a = $('<a></a>').text(e["stock_name"]).addClass('nav-item nav-link').attr('href', '#');
                a.append($('<br>'))
                a.append($('<span id=rt'+e['stock_id']+'>').addClass('nav-link'))
                a.click(function () {
                    clearTimeout(loopflag)
                    ul.children().removeClass('active')
                    this.classList.add("active");
                    console.log("getting " + e["stock_name"])
                    // $.get("/data",e,plotChart,"json")
                    // let url = "/static/testdata/" + e["stock_name"] + ".json";
                    let url = "/stockdata?type=history&name=" + e["stock_name"];
                    $.get(url, plotHis, "json");
                    url = '/long?name=' + e["stock_name"]
                    $.get(url,plotIndicator,'json')
                    realTimeLoop(e["stock_name"])
                });
                ul.append(a);
            });
        },
        error: function () {
            alert('error');
        }

    })
});