$(function () {
    var html = '';
    html += '<div id="tcc_phone_id" style="width:70%;height:auto;padding:15px;position:fixed;left:50%;margin-left:-35%;top:50%;margin-top:-175px;background:#fff;display:none;z-index:10000;text-align:center;line-height:80px;border-radius:8px;">';
    html += '<span id="spansd_id" style="display:block;border-bottom: solid 1px #ddd;line-height: 1.5;padding: 5% 0;height: auto;word-wrap:break-word;text-align:center; ">请先关注公众号</span>';
    html += '<a href="javascript:;" style="display:block;width:100px;height:35px;font-size:14px;color:#fff;line-height:35px;text-align:center;background:#66B3FF;border-radius:4px;margin:0 auto;margin-top: 6%;" onclick="asureFun();">确定</a>';
    html += '</div>';
    html += '<div id="phone_bg_id" style="background:rgba(0,0,0,0.5);display:none;position:fixed;left:0;top:0;width:100%;height:100%;z-index:1000;"></div>';
    $("body").append(html);
});

//alert重组

function alert_(m) {
    $("#spansd_id").html(m);
    $("#tcc_phone_id").show();
    $("#phone_bg_id").show();
}

function asureFun(mark) {
    $("#spansd_id").html('');
    $("#tcc_phone_id").hide();
    $("#phone_bg_id").hide();
}

//资讯论坛，权限判断
function checkUserPower(code) {
    $.post('/index.php/Home/Base/checkUserPower', {code: code}, function (data) {
        if (!data.flag) {
            alert(data.msg);
        } else {
            goTo("/index.php/Home/Infoforum/infodetail/code/" + code);
            //$("#openWin").attr("action",url);
            //$("#openWin").submit();
        }
    }, 'json');
}
function goTo(url) {
    //alert(123);return false;
    var newA = document.createElement("a");
    newA.id = 'gg'
    newA.target = '_blank';
    newA.href = url;
    document.body.appendChild(newA);
    newA.click();
    document.body.removeChild(newA);
}
//统计，权限判断
function statisticsCheckUserPower(code, mark) {
    $.post('/index.php/Home/Base/statisticsCheckUserPower', {mark: mark}, function (data) {
        //var tempwindow=window.open('_blank');
        if (!data.flag) {
            alert(data.msg);
        } else {
            if (mark == "Y") {
                //月报详情页
                goTo("/index.php/Home/Datastatistics/monthlyInfo/si_code/" + code);
                //var url = "/index.php/Home/Datastatistics/monthlyInfo/si_code/"+code;
                // tempwindow.location="/index.php/Home/Datastatistics/monthlyInfo/si_code/"+code;
                //$("#openWin").attr("action",url);
                //$("#openWin").submit();
            } else if (mark == "T") {
                //进出口详情页
                goTo("/index.php/Home/Datastatistics/importExporInfo/siei_code/" + code);
                //var url = "/index.php/Home/Datastatistics/importExporInfo/siei_code/"+code;
                ////$("#openWin").attr("action",url);
                //$("#openWin").submit();
                //tempwindow.location="/index.php/Home/Datastatistics/importExporInfo/siei_code/"+code;
            } else if (mark == "D") {
                //月报查询列表
                goTo("/index.php/Home/Datastatistics/monthlyRead");
                //var url = "/index.php/Home/Datastatistics/monthlyRead";
                //$("#openWin").attr("action",url);
                //$("#openWin").submit();
                //tempwindow.location="/index.php/Home/Datastatistics/monthlyRead";
            }
        }
    }, 'json');
}