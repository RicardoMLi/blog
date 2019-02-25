function getCookie(name) {
     var cookieValue = null;
     if (document.cookie && document.cookie != '') {
         var cookies = document.cookie.split(';');
         for (var i = 0; i < cookies.length; i++) {
             var cookie = jQuery.trim(cookies[i]);
             // Does this cookie string begin with the name we want?
             if (cookie.substring(0, name.length + 1) == (name + '=')) {
                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                 break;
             }
         }
     }
     return cookieValue;
}

// is_parent为true则跳转父级类别
function goto_category(id, is_parent) {
    if(typeof id != 'number')
        return;

    $.ajax({
        url: '/category/find_parent/',
        type: 'GET',
        data: {'id': id, 'is_parent': is_parent},
        cache: false,
        success: function (data) {
            if(data.status == 'success'){
                window.location.href = data.msg;
            }
        }
    })

}

function check_name(name){
    if(name.length == 0)
        return '用户名不能为空'

    if(name.length < 3 || name.length > 20)
        return '用户名长度为3-20位';

    return true;
}

function check_password(password){
    if(password.length == 0)
        return '密码不能为空';

    if(password.length < 5 || password.length > 18)
        return '密码长度为5-18位';

    return true;

}

$('#name').focus(function () {
    if($('.error-output label').length != 0)
        $('.error-output').empty();
});

// 检查用户名是否被注册
$('#name').blur(function () {
    var name = $('#name').val();

    if(name === ''){
        $('.error-output').append($('<label></label>').addClass('btn btn-danger').css('width', '100%').text('用户名不能为空'));
        return;
    }

    $.ajax({
        url: '/user/check_name/',
        data: {'name': name},
        type: 'GET',
        cache: false,
        async: true,
        success: function (data) {
            if(data.status === 'fail')
                $('.error-output').append($('<label></label>').addClass('btn btn-danger').css('width', '100%').text(data.msg));

        }

    })

});

$('#email').focus(function () {
    if($('.error-output label').length != 0)
        $('.error-output').empty();
});

// 检查邮箱是否被注册
$('#email').blur(function () {
    var email = $('#email').val();

    if(email === ''){
        $('.error-output').append($('<label></label>').addClass('btn btn-danger').css('width', '100%').text('邮箱不能为空'));
        return;
    }

    $.ajax({
        url: '/user/check_email/',
        data: {'email': email},
        type: 'GET',
        async: true,
        cache: false,
        success: function (data) {
            if(data.status === 'fail')
                $('.error-output').append($('<label></label>').addClass('btn btn-danger').css('width', '100%').text(data.msg));
        }
    });

});

function register () {

    //移除error-output子元素
    if($('.error-output label').length != 0){
        $('.error-output').empty();
    }

    var csrftoken = getCookie('csrftoken');
    var name = $('.jsRegisterName').val();
    var email = $('.jsRegisterEmail').val();
    var password = $('.jsRegisterPassword').val();
    var re_password = $('.jsRegisterRePassword').val();
    var reg =  /^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$/;

    var name_result = check_name(name);
    if(!name_result){
        $('.error-output').append($('<label></label>').addClass('btn btn-danger').css('width', '100%').text(name_result));
        return;
    }

    if(!reg.test(email)){
        $('.error-output').append($('<label></label>').addClass('btn btn-danger').css('width', '100%').text('邮箱地址格式错误'));
        return;
    }

    var password_result = check_password(password);

    if(!password_result){
        $('.error-output').append($('<label></label>').addClass('btn btn-danger').css('width', '100%').text(password_result));
        return;
    }

    if(password !== re_password){
        $('.error-output').append($('<label></label>').addClass('btn btn-danger').css('width', '100%').text('两次输入的密码不一致'));
        return;
    }

    $("#jsRegisterButton").attr("disabled", "disabled");
    $("#jsRegisterButton").val("正在注册中...");

    $.ajax({
        url: '/user/register/',
        type: 'POST',
        data: $('.jsRegisterForm').serialize(),
        cache: false,
        async: true,
        dataType: 'json',
        beforeSend:function(xhr, settings){
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        success: function (data) {
            if(data.status == 'success'){
                window.location.href = data.return_url;
            }else{
                $("#jsRegisterButton").removeAttr("disabled");
                $('#jsRegisterButton').val("注册");
                $('.jsRegisterName').val("");
                $('.jsRegisterEmail').val("");
                $('.jsRegisterPassword').val("");
                $('.jsRegisterRePassword').val("");
            }
        }
    });
}

$('#jsLoginForm').submit(function (e) {
    e.preventDefault();
    //移除error-output子元素
    if($('.error-output label').length != 0){
        $('.error-output').empty();
    }

    $("#jsLoginButton").attr("disabled", "disabled");
    $("#jsLoginButton").val("正在登陆中...");

    var csrftoken = getCookie('csrftoken');

    $.ajax({
        url: '/user/login/',
        type: 'POST',
        data: $('#jsLoginForm').serialize(),
        cache: false,
        async: true,
        dataType: 'json',
        beforeSend:function(xhr, settings){
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        success: function (data) {
            if(data.status == 'fail'){
                var msg = data.msg;
                $("#jsLoginButton").removeAttr("disabled");
                $('.error-output').append($('<label></label>').addClass('btn btn-danger').css('width', '100%').text(msg['__all__'].pop()));
                $("#password").val("");
                $("#jsLoginButton").val("登陆");
            }else{
                $("#jsLoginButton").removeAttr("disabled");
                window.location.href = data.msg;
            }
        }
    });
    return false;
});

// 点赞js

(function($) {
    $.extend({
        tipsBox: function(options) {
            options = $.extend({
                obj: null,
                str: "+1",
                startSize: "12px",
                endSize: "30px",
                interval: 600,
                color: "red",
                callback: function() {}
            },
            options);
            $("body").append("<span class='num'>" + options.str + "</span>");
            var box = $(".num");
            var left = options.obj.offset().left + options.obj.width() / 2;
            var top = options.obj.offset().top - options.obj.height();
            box.css({
                "position": "absolute",
                "left": left + "px",
                "top": top + "px",
                "z-index": 9999,
                "font-size": options.startSize,
                "line-height": options.endSize,
                "color": options.color
            });
            box.animate({
                "font-size": options.endSize,
                "opacity": "0",
                "top": top - parseInt(options.endSize) + "px"
            },
            options.interval,
            function() {
                box.remove();
                options.callback()
            })
        }
    })
})(jQuery);

$.fn.postLike = function() {
    if ($(this).hasClass("actived")) {
        return alert("已经点过赞啦，记性差还是手贱呢！")
    } else {
        $(this).addClass("actived");
        var csrftoken = getCookie('csrftoken');
        var id = $(this).data("id"),
        action = $(this).data("action"),
        rateHolder = $(this).children(".count");
        var ajax_data = {
            action: "like",
            um_id: id,
            um_action: action
        };
        $.ajax({
            url: '/blog/add_like/',
            type: 'POST',
            data: ajax_data,
            beforeSend:function(xhr, settings){
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            success: function (data) {
                $(rateHolder).html(data.like_count);
            }
        });
        $.tipsBox({
            obj: $(this),
            str: "+1",
            callback: function() {}
        });

        return false;
    }
};

$(document).on("click", "#Addlike",
function() {
    $(this).postLike()
});

// 留言js

String.prototype.format = function() {
    var str = this ;
    for (var i = 0; i < arguments.length; i++) {
        var str = str.replace(new RegExp('\\{' + i + '\\}','g'),arguments[i]);
    }
    return str;
};

function numFormat(num) {
    return ('00' + num).substr(-2) ;
}

function formatTime(timestamp) {
    var datetime = new Date(timestamp*1000);
    var year = datetime.getFullYear();
    var month = numFormat(datetime.getMonth() + 1);
    var day = numFormat(datetime.getDate());
    var hour = numFormat(datetime.getHours());
    var minute = numFormat(datetime.getMinutes());

    return year + '-' + month + '-' + day + ' ' + hour + ':' + minute;
}


function back_to_edit(message_id, user_id ,type) {
    $('html').animate({scrollTop: $('#comment').offset().top-200},500,function () {
        $('#comment').focus();
    });
    if(type == 'message'){
        $("#to_user_id").val(user_id);
        $("#message_id").val(message_id);
    }else{
        $("#parent_id").val(message_id);
        $("#to_user_id").val(user_id);
    }

}

function addRootMessage(msg) {
    var rootMessage_html = "<li class=\"comment\" id=\"{5}\">\n" +
        "                        <div class=\"c-avatar\">\n" +
        "                            <img alt='默认图片'  src=\"http://127.0.0.1:8000/static/img/default.png\" class='avatar' height='54' width='54' />\n" +
        "                            <div class=\"c-main\">{0}\n" +
        "                                <div class=\"c-meta\">\n" +
        "                                    <span class=\"c-author\">\n" +
        "                                        <span rel='external nofollow' class='url'>{1}</span>\n" +
        "                                    </span>{2}\n" +
        "                                    <a rel='nofollow' href='javascript:back_to_edit({3},{4},\"{6}\")' class='comment-reply-link'>回复</a>\n" +
        "                                </div>\n" +
        "                            </div>\n" +
        "                        </div>\n" +
        "<ul class=\"children\">"+"</ul>" +
        "                    </li>";
    if(msg.hasOwnProperty('parent_id')){
        rootMessage_html = rootMessage_html.format(msg['comment'], msg['username'], formatTime(msg['time']), msg['comment_id'], msg['user_id'], msg['comment_tag_id'], "comment");
        $('.commentlist').prepend(rootMessage_html);
    }else{
        rootMessage_html = rootMessage_html.format(msg['message'], msg['username'], formatTime(msg['time']), msg['message_id'], msg['user_id'], msg['comment'], "message");
        $('.commentlist').prepend(rootMessage_html);
    }

}

function addChildMessage(msg) {
    var childMessage_html = "<li class=\"comment\" id=\"{5}\">\n" +
        "                                <div class=\"c-avatar\">\n" +
        "                                    <img alt='' src=\"http://127.0.0.1:8000/static/img/default.png\" class='avatar' height='54' width='54' />\n" +
        "                                    <div class=\"c-main\">{0}\n" +
        "                                        <div class=\"c-meta\">\n" +
        "                                            <span class=\"c-author\">\n" +
        "                                                <span rel='external nofollow' class='url'>{1}</span>\n" +
        "                                            </span>{2}\n" +
        "                                            <a rel='nofollow' class='comment-reply-link' href='javascript:back_to_edit({3},{4},\"{6}\")'>回复</a>\n" +
        "                                        </div>\n" +
        "                                    </div>\n" +
        "                                </div>\n" +
        "<ul class=\"children\">"+"</ul>" +
        "                            </li>";

    if(msg.hasOwnProperty('parent_id')){
        // 评论
        childMessage_html = childMessage_html.format(msg['comment'], msg['username'], formatTime(msg['time']), msg['comment_id'], msg['user_id'], "message_{0}".format(msg['comment_id']), "comment");
        $("#{0} .children:eq(0)".format(msg['comment_tag_id'])).prepend(childMessage_html);
    }else{
        // 留言
        childMessage_html = childMessage_html.format(msg['message'], msg['username'], formatTime(msg['time']), msg['message_id'], msg['user_id'], msg['message_comment_id'], "message");
        $("#{0} .children:eq(0)".format(msg['comment'])).prepend(childMessage_html);
    }

}

function addMessage(id) {
    $(".comt-loading").show();
    var comment = $.trim($("#comment").val());

    if(typeof id != "number"){
        alert("您还未登录哦，请先登录再给我留言吧");
        return;
    }

    if(comment == ''){
        alert("评论内容不能为空!");
        return;
    }
    var txt1 = '<div class="comt-tip comt-loading">正在提交, 请稍候...</div>';
    var txt2 = '<div class="comt-tip comt-error"></div>';
    $(".comt-tips").append(txt1 + txt2);
    $('#submit').attr("disabled", true).fadeTo("slow", 0.5);

    $.ajax({
        url: '/category/message/',
        type: 'POST',
        data:$("#messageform").serialize(),
        error: function (data) {
            $(".comt-loading").hide();
            $(".comt-error").show().html(data.msg);
            setTimeout(function() {
                $("#messageform #submit").attr("disabled", false).fadeTo("slow", 1);
                $(".comt-error").fadeOut();
            },
            3000);
        },
        success: function (data) {
            $(".comt-loading").hide();
            $('#comment').val("");
            if(data.status == 'success'){
                $('#submit').attr("disabled", false).fadeTo("slow", 1);
                $(".comt-loading").remove();
                $(".comt-error").remove();
                var msg = data.msg;
                if(msg['reply'] === 'yes'){
                    addChildMessage(msg);
                    $('html').animate({scrollTop: $("#{0}".format(msg['message_comment_id'])).offset().top }, 500);
                }else{
                    addRootMessage(msg);
                    $('html').animate({scrollTop: $("#comment_{0}".format(msg['message_id'])).offset().top }, 500);
                }
            }else{
                $(".comt-loading").hide();
                $('.comt-error').text(data.msg);
                setTimeout(function() {
                   $('.comt-error').fadeOut();
                }, 6000);
                $('#submit').attr("disabled", false).fadeTo("slow", 1);
            }
        }
    });
    return false;
}

// 评论js
function addComment (id) {
    $(".comt-loading").show();
    var comment = $.trim($("#comment").val());

    if(typeof id != "number"){
        alert("您还未登录哦，请先登录再评论吧");
        return;
    }

    if(comment == ''){
        alert("评论内容不能为空!");
        return;
    }
    var txt1 = '<div class="comt-tip comt-loading">正在提交, 请稍候...</div>';
    var txt2 = '<div class="comt-tip comt-error"></div>';
    $(".comt-tips").append(txt1 + txt2);
    $('#submit').attr("disabled", true).fadeTo("slow", 0.5);

    $.ajax({
        url: '/comment/add/',
        type: 'POST',
        data: $("#commentform").serialize(),
        error: function (data) {
            $(".comt-loading").hide();
            $(".comt-error").show().html(data.msg);
            setTimeout(function() {
                $("#submit").attr("disabled", false).fadeTo("slow", 1);
                $(".comt-error").fadeOut();
            },
            3000);
        },
        success: function (data) {
            $(".comt-loading").hide();
            $('#comment').val("");
            if(data.status == 'success'){
                $('#submit').attr("disabled", false).fadeTo("slow", 1);
                $(".comt-loading").remove();
                $(".comt-error").remove();
                var msg = data.msg;
                if(msg['parent_id'] == ''){
                    addRootMessage(msg);
                    $('html').animate({scrollTop: $("#{0}".format(msg['comment_tag_id'])).offset().top }, 500);
                }else{
                    addChildMessage(msg);
                    $('html').animate({scrollTop: $("#{0}".format(msg['comment_tag_id'])).offset().top }, 500);
                }
            }else{
                $(".comt-loading").hide();
                $('.comt-error').text(data.msg);
                setTimeout(function() {
                   $('.comt-error').fadeOut();
                }, 6000);
                $('#submit').attr("disabled", false).fadeTo("slow", 1);
            }
        }
    });
    return false;
}

// 留言处分享
function share_at_message(option) {
    var content = "欢迎分享念旧博客，您的赞赏是对我最大的鼓励。博客地址:http://127.0.0.1:8000/";
    var url = window.location.href;
    var sharestring = "";

    if(typeof option != 'number'){
        return;
    }

    if(option == 1){
        sharestring = 'http://v.t.sina.com.cn/share/share.php?title='+content+'&url='+url+'&content=utf-8&sourceUrl='+url;
    }else if(option == 2){
        sharestring = 'http://sns.qzone.qq.com/cgi-bin/qzshare/cgi_qzshare_onekey?summary='+title+'&url='+url;
    }else if(option == 3){
        sharestring = 'http://v.t.qq.com/share/share.php?title='+content+'&url='+url;
    }else if(option == 4){
        sharestring = 'https://connect.qq.com/widget/shareqq/index.html?url='+url+'&title='+content;
    }else if(option == 5){
        sharestring = 'http://widget.renren.com/dialog/share?resourceUrl='+url+'&srcUrl='+url+'&title='+content;
    }else if(option == 6){
        sharestring = '';
    }else{
        return;
    }

    window.open(sharestring, 'newwindow', 'height=400,width=400,top=100,left=100');
}

// 博客处分享
function share_at_blog(option) {
    var content = $("#blog_title").text();
    var id = $("#blog_title").attr("blog_id");
    var url = window.location.href;
    var sharestring = "";

    if(typeof option != 'number'){
        return;
    }

    if(option == 1){
        sharestring = 'http://v.t.sina.com.cn/share/share.php?title='+content+'&url='+url+'&content=utf-8&sourceUrl='+url;
    }else if(option == 2){
        sharestring = 'http://sns.qzone.qq.com/cgi-bin/qzshare/cgi_qzshare_onekey?summary='+title+'&url='+url;
    }else if(option == 3){
        sharestring = 'http://v.t.qq.com/share/share.php?title='+content+'&url='+url;
    }else if(option == 4){
        sharestring = 'https://connect.qq.com/widget/shareqq/index.html?url='+url+'&title='+content;
    }else if(option == 5){
        sharestring = 'http://widget.renren.com/dialog/share?resourceUrl='+url+'&srcUrl='+url+'&title='+content;
    }else if(option == 6){
        sharestring = '';
    }else{
        return;
    }

    // 暂时不检测分享是否成功
    $.ajax({
        url:'/blog/share/',
        type: 'GET',
        data: {'id': id},
        async: true,
        success: function (data) {
            if(data.status == 'success'){
                $("#share_times").text(data.msg);
            }
        }
    });

    window.open(sharestring, 'newwindow', 'height=400,width=400,top=100,left=100');
}



