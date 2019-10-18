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
          textarea: $('#R_editor'),
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

    (function() {
      $(function() {
        var editor,toolbar;
        Simditor.locale = 'zh-CN';
        toolbar = ['title', 'bold', 'italic', 'underline',
            'strikethrough', 'fontScale', 'color', '|',
            'ol', 'ul', 'blockquote', 'code', 'table',
            '|', 'link', 'image', 'hr', '|', 'indent',
            'outdent', 'alignment'];

        editor = new Simditor({
          textarea: $('#W_editor'),
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

$(function() {
    var editor,toolbar;
    Simditor.locale = 'zh-CN';
    toolbar = ['title', 'bold', 'italic', 'underline', 'strikethrough',
    'fontScale', 'color', '|', 'ol', 'ul', 'blockquote',
    'code', 'table', '|', 'link', 'image', 'hr', '|',
    'indent', 'outdent', 'alignment'];
    editor = new Simditor({
    textarea: $('#M_editor'),
    placeholder: '这里输入题目内容...',
    toolbar: toolbar,
    pasteImage: true,
    upload: {
        url: '/upload/',
        params: null,
        fileKey: "upload_file",
        connectionCount: 3,
        leaveConfirm: "正在上传,确定要取消上传文件吗?"
        }
    });
});

function addbutton_all_R(obj){
	html = '<div class="input-group saltIp" style="width:100%;padding:0 0 1px 0;">'+
						'<label class="input-group-addon">选项:</label>'+
						'<input type="text" class="form-control" id="R_all_answers" name="R_all_answer" style="width:500px;" required>'+
						'<span class="input-group-btn">'+
    						'<button class="btn btn-info" type="button" data-toggle="tooltip" title="删除" id="delbutton_all_R" ><span class="glyphicon glyphicon-minus"></span></button>'+
    					'</span>'+
					'</div>';
	obj.insertAdjacentHTML('beforebegin',html)
}


$(document).on('click','#delbutton_all_R',function(){
	var el = this.parentNode.parentNode;
	var saltIp = $(this).parent().parent().find('#R_all_answers').val();
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

function addbutton_all_M(obj){
	html = '<div class="input-group saltIp" style="width:100%;padding:0 0 1px 0;">'+
						'<label class="input-group-addon">选项:</label>'+
						'<input type="text" class="form-control" id="M_all_answers" name="M_all_answer" style="width:500px;" required>'+
						'<span class="input-group-btn">'+
    						'<button class="btn btn-info" type="button" data-toggle="tooltip" title="删除" id="delbutton_all_M" ><span class="glyphicon glyphicon-minus"></span></button>'+
    					'</span>'+
					'</div>';
	obj.insertAdjacentHTML('beforebegin',html)
}


$(document).on('click','#delbutton_all_M',function(){
	var el = this.parentNode.parentNode;
	var saltIp = $(this).parent().parent().find('#M_all_answers').val();
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
	})

});

