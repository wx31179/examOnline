var requesta;
var requestb;
$(document).ready(function() {
    (function() {
      $(function() {
        var editor,toolbar;
        Simditor.locale = 'zh-CN';
        toolbar = ['title', 'bold', 'italic', 'underline', 'strikethrough',
            'fontScale', 'color', '|', 'ol', 'ul', 'blockquote', 'code',
            'table', '|', 'link', 'image', 'hr', '|', 'indent', 'outdent',
            'alignment'];

        editor = new Simditor({
          textarea: $('#editor'),
          placeholder: '这里输入题目内容...',
          toolbar: toolbar,
          pasteImage: true,
          defaultImage: '/simditor/images/image.png',
          upload: {
            url: '/upload/',
            params: null,
            fileKey: "upload_file",
            connectionCount: 3,
            leaveConfirm: "正在上传,确定要取消上传文件吗?"
          }
        });
      });

    }).call(this);

});
function addbutton_all(obj){
	html = '<div class="input-group saltIp" style="width:100%;padding:0 0 1px 0;">'+
						'<label class="input-group-addon">选项:</label>'+
						'<input type="text" class="form-control" id="all_answers" name="all_answer" style="width:500px;" required>'+
						'<span class="input-group-btn">'+
    						'<button class="btn btn-info" type="button" data-toggle="tooltip" title="删除" id="delbutton_all" ><span class="glyphicon glyphicon-minus"></span></button>'+
    					'</span>'+
					'</div>';
	obj.insertAdjacentHTML('beforebegin',html)
}


$(document).on('click','#delbutton_all',function(){
	var el = this.parentNode.parentNode;
	var saltIp = $(this).parent().parent().find('#all_answers').val();
	if (saltIp === ""){
		el.parentNode.removeChild(el);
		return
	}
	alertify.confirm('您确定要删除选中的命令？',
	function(e){
		if(e){
			$.ajax({
				'url':'/url',
				'type':'POST',
				'async':false,
				'dataType':'json',
				'data':{'type':'delSaltIp','projectId':projectId,'saltIp':saltIp},
				'success':function(result){
					if (result.code){
						el.parentNode.removeChild(el)
					}else {
						showError(result.msg)
					}
				}
			})

		}
	})

});

function addbutton_right(obj){
	html = '<div class="input-group saltIp" style="width:100%;padding:0 0 1px 0;">'+
						'<label class="input-group-addon">选项:</label>'+
						'<input type="text" class="form-control" id="M_right_answers" name="M_right_answer" style="width:500px;" required>'+
						'<span class="input-group-btn">'+
    						'<button class="btn btn-info" type="button" data-toggle="tooltip" title="删除" id="delbutton_right" ><span class="glyphicon glyphicon-minus"></span></button>'+
    					'</span>'+
					'</div>';
	obj.insertAdjacentHTML('beforebegin',html)
}


$(document).on('click','#delbutton_right',function(){
	var el = this.parentNode.parentNode;
	var saltIp = $(this).parent().parent().find('#M_right_answers').val();
	if (saltIp === ""){
		el.parentNode.removeChild(el);
		return
	}
	alertify.confirm('您确定要删除选中的命令？',
	function(e){
		if(e){
			$.ajax({
				'url':'/url',
				'type':'POST',
				'async':false,
				'dataType':'json',
				'data':{'type':'delSaltIp','projectId':projectId,'saltIp':saltIp},
				'success':function(result){
					if (result.code){
						el.parentNode.removeChild(el)
					}else {
						showError(result.msg)
					}
				}
			})

		}
	});

});

function diff_exam() {
	var right_answer=document.getElementsByName("right_answer");
   var all_answer = document.getElementsByName("all_answer");
   var content = document.getElementsByName("content");
   var project = document.getElementsByName("project");
   var answers = [];
   for (var k=0;k<content.length;k++){
   		for (var h=0;h<project.length;h++){
   			if(content[k].value==="" || project[h].value===""){
   				alert("内容或项目不能为空")

			} else {
   				if(requestb!=="W"){
					for (var j = 0; j < all_answer.length; j++) {
						answers.push(all_answer[j].value);
					}
				   var flag;
				   for (var i = 0; i < right_answer.length; i++) {
						if (answers.indexOf(right_answer[i].value)===-1){
							flag = false;
							break
						}else {
							flag=true
						}
				   }
				   if(flag){
						if(confirm("确认修改吗")){
							$("#form").submit()
						} else{
							return false
						}
				   } else {
					   alert("答案与选项不符合")
				   }
			   	}else {
   					if(confirm("确认修改吗")){
   						$("#form").submit()
					} else{
   						return false
					}


			   	}
			}
		}

   }



}

