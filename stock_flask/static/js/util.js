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
                gridLines: {
                    color: "rgba(255,255,255,0.2)"
                }
            }]
        }
    };
    var chart1 = new Chart(ctx1, { type: "line", options: option })
    var chart2 = new Chart(ctx2, { type: "line", options: option })
    function plotHis(dataJson) {
        if (chart1) chart1.destroy();
        name = dataJson['name'];
        labels = dataJson['timestamp'];
        labels = labels.map(i => i * 1000);
        data = dataJson['close'];
        chart1 = new Chart(ctx1, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: "History",
                    backgroundColor: "rgba(255,255,255,0.1)",
                    borderColor: "rgba(255,255,255,0.5)",
                    data: data,
                    pointRadius: 1,
                }]
            },
            options: option,
        })
        let his = $("#historically").children().removeClass('zero')
        his[0].innerText = Math.max.apply(null, dataJson['high'])
        his[1].innerText = Math.min.apply(null, dataJson['low'])
    }
    function plotReal(dataJson) {
        if (chart2) chart2.destroy();
        name = dataJson['name'];
        labels = dataJson['timestamp'];
        labels = labels.map(i => i * 1000);
        close = dataJson['close'];
        high = dataJson['high'];
        low = dataJson['low'];
        chart2 = new Chart(ctx2, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    type: 'line',
                    label: 'Real Time',
                    backgroundColor: "rgba(255,255,255,0.1)",
                    borderColor: "rgba(255,255,255,0.5)",
                    data: close,
                    pointRadius: 1
                }, {
                    label: 'high',
                    backgroundColor: "rgba(0,205,0,0.1)",
                    borderColor: "rgba(0,205,0,0.5)",
                    data: high,
                    fill: false,
                    showLine: false,
                    pointStyle: 'cross',
                    pointRadius: 3,
                }, {
                    label: 'low',
                    backgroundColor: "rgba(205,0,0,0.1)",
                    borderColor: "rgba(205,0,0,0.5)",
                    data: low,
                    fill: false,
                    showLine: false,
                    pointStyle: 'line',
                    pointRadius: 3,
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
                        gridLines: {
                            color: "rgba(255,255,255,0.2)"
                        }
                    }]
                }
            },
        })
    }
    var loopflag;
    var rand = () => Math.random() * 100 + 10;
    function addRealLoop(name) {
        console.log("getting realtime " + name);
        let url = "/getStock/real/" + name;
        $.get(url, plotReal, "json")
        // loopflag = setTimeout(function () { addRealLoop(name), 60000 })
        // $.ajax({
        //     type: 'GET',
        //     timeout: 10000,
        //     dataType: 'json',
        //     // url: "/realtime",
        //     // data: name,
        //     url: "/static/testdata/realtime.json",
        //     success: function (result) {
        //         let pre = $('#predict').children().removeClass('zero')
        //         let realtime = $('#realtime').children().removeClass('zero')
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
        url: "/getStock",
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
                    let url = "/getStock/" + e["stock_name"];
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
    // console.log('hghh') 
    // char = new Chart(ctx, {
    //     type: 'line',
    //     data: {
    //         labels: [1550759400.0, 1551105000.0, 1576852200],
    //         datasets: [{
    //             label: "nvida",
    //             backgroundColor:"rgba(255,255,255,0.1",
    //             borderColor:"rgba(255,255,255,0.5",
    //             data: [12, 20,50]
    //         }]
    //     },
    //     options: {
    //         scales: {
    //             xAxes: [{
    //                 type: 'time',
    //                 time: {
    //                 displayFormats: {
    //                     week: 'll'
    //                 }
    //                 },
    //                 gridLines: {
    //                     color:"rgba(255,255,255,0.2)"
    //                 },
    //                 time: {
    //                     unit: 'day'
    //                 }
    //             }],
    //             yAxes: [{
    //                 gridLines: {
    //                     color:"rgba(255,255,255,0.2)"
    //                 }
    //             }]
    //         }
    //     }
    // })
    // char.data.labels.push(1582813800);
    // char.data.datasets.forEach((dataset) => {
    //     dataset.data.push(60);
    // });
    // char.update()
});