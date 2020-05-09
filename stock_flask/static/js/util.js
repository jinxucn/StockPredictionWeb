/*
 * @Author: Jin X
 * @Date: 2019-11-27 15:58:08

 */


$(function () {
    var ctx1 = $('#chart1')
    var ctx2 = $('#chart2')
    var option = {
        scales: {
            xAxes: [{
                type: 'time',
                time: {
                    // displayFormats: {
                    //     quarter: 'll'
                    // },
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
        his[0].innerText = Math.max.apply(null, dataJson['high'])
        his[1].innerText = Math.min.apply(null, dataJson['low'])
    }
    function plotReal(dataJson) {
        if (chart2) chart2.destroy();
        let name = dataJson['name'];
        let labels = dataJson['timestamp'];
        labels = labels.map(i => i * 1000);
        let volume = dataJson['volume'];
        volume[0] = 0;
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
    function addRealLoop(name) {
        console.log("getting realtime " + name);
        let url = "/stockdata?type=realtime&name=" + name;
        $.get(url, plotReal, "json")
        loopflag = setTimeout(function () { addRealLoop(name) }, 60000)
        // $.ajax({
        //     type: 'GET',
        //     timeout: 10000,
        //     dataType: 'json',
        //     // url: "/realtime",
        //     // data: name,
        //     url: "/static/testdata/realtime.json",
        //     success: function (result) {
        //         let pre = $('#predict').children().removeClass('zero')
        // let realtime = $('#realtime').children().removeClass('zero')
        //         // pre[0].innerText=result["pre5minutes"]
        //         // pre[1].innerText=result["pre3days"]
        //         pre[0].innerText = rand()
        //         pre[1].innerText = rand()
        //         for (let i = 0; i < realtime.length; i++) {
        //             realtime[i].innerText = rand()
        //             // realtime[i].innerText=result["realtime"][i]
        //         }

        //         // loopflag=setTimeout(function(){addRealLoop(name)},5000)
        //         loopflag = setTimeout(function () { addRealLoop(name) }, 60000)
        //     }
        // })
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
                a.click(function () {
                    clearTimeout(loopflag)
                    ul.children().removeClass('active')
                    this.classList.add("active");
                    console.log("getting " + e["stock_name"])
                    // $.get("/data",e,plotChart,"json")
                    // let url = "/static/testdata/" + e["stock_name"] + ".json";
                    let url = "/stockdata?type=history&name=" + e["stock_name"];
                    $.get(url, plotHis, "json");
                    addRealLoop(e["stock_name"])
                });
                ul.append(a);
            });
        },
        error: function () {
            alert('error');
        }

    })
    $('#nav-fig').click(function () {
        $('#nav-fig').addClass('active')
        $('#nav-sum').removeClass('active')
        $('#page-fig').show()
        $('#page-sum').hide()
    })
    function getSum() {
        $tb = $('#tb')
        $tb.bootstrapTable('showLoading');
        var timeBegin = new Date();
        $.ajax({
            type: "GET",
            timeout: 10000,
            dataType: "json",
            url: "/summary",
            success: function (result) {
                $tb.bootstrapTable('destroy');
                var $tr = $('#colh').find('tr')
                $tr.children().remove();
                var first = result[0];
                Object.keys(first).forEach(function (e) {
                    $tr.append($('<th></th>').text(e).attr('data-field', e))
                })
                $tb.bootstrapTable();
                $tb.bootstrapTable('load', result);
                $tb.bootstrapTable('hideLoading')
                console.log('load data')
            },
            error: function () {
                alert("error");
            }
        });
    };
    $('#nav-sum').click(function () {
        $('#nav-sum').addClass('active')
        $('#nav-fig').removeClass('active')
        $('#page-sum').show()
        $('#page-fig').hide()
        getSum();
    })
});