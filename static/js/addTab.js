   function addTab(id,tag,name) {
        var tab_exist = document.getElementById(tag);
        if(tab_exist){
            tab_exist.click()
        }else {
            var a = document.getElementById("tab_tittle").innerHTML;
            document.getElementById("tab_tittle").innerHTML = a+'<li><a id='+'"'+tag+'"'+ ' data-toggle="tab" href="'+'#'+id+'"'+'>'+name+'</a></li>';
            var b = document.getElementById("tab_container").innerHTML;
            document.getElementById("tab_container").innerHTML = b+'    <div id="'+id+'"'+' class="tab-pane fade">\n' +
                                                                            '<div class="embed-responsive embed-responsive-4by3">\n'+
                                                                                '<iframe scrolling="auto" src='+'/'+id+'/'+ '>\n'+
                                                                                '</iframe>\n'+
                                                                            '</div>\n' +
                                                                            '    </div>';

            document.getElementById(tag).click()
        }

    }