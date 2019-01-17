$(function() {
    var editor = ace.edit("editor");
    editor.session.setMode("ace/mode/python");
    function getcode(){
        code = editor.getValue();
        return code
    }
    editor.session.on('change', function(delta) {
        $("#codefield").val(getcode());
    });
    $('#input-tags').selectize({
        delimiter: ',',
        persist: false,
        create: function(input) {
            return {
                value: input,
                text: input
            }
        }
    });
})

var doc = document;
function showinput(comm_id)
{
    var comment = doc.getElementById(comm_id);
    var id = comment.dataset.commentId;
    doc.getElementById(""+id+"comment").style.display = 'none';
    doc.getElementById(""+id+"editcomment").style.display = 'inline';
}
function hideinput(comm_id)
{
    var comment = doc.getElementById(comm_id);
    var id = comment.dataset.commentId;
    doc.getElementById(""+id+"comment").style.display = 'block';
    doc.getElementById(""+id+"editcomment").style.display = 'none';
}
function reply(comm_id)
{
    var comment = doc.getElementById(comm_id);
    var name = comment.dataset.commentName;
    var field = doc.getElementById('comment-field');
    field.value = name + ", ";
    var reply_to = doc.getElementById('reply_to');
    var id = comment.dataset.commentId;
    reply_to.value = id;
}
