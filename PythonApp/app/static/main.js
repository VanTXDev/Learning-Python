$(document).ready(function () {
	setTaskCompletedStyle();
	$(".ckb-completed").click(function (e) {
		e.preventDefault();
		var isCompleted = $(this).prop("checked");
		var inputName = $(this).attr("name");
		var taskId = inputName.slice(12, inputName.length);
		setCompleteStatus(taskId, isCompleted);
	});
});
function setCompleteStatus(taskId, isCompleted) {
	$.ajax({
		url: "/set_complete",
		method: "POST",
		contentType: "application/json",
		data: JSON.stringify({
			task_id: taskId,
			is_completed: isCompleted
		}),
		dataType: "json",
		success: function (response) {
			console.log(response);
			$(`#is_completed${taskId}`).prop("checked", response.is_completed);
			setTaskCompletedStyle(taskId, response.is_completed);
		},
		error: function (e) {
			console.log(e);
		}
	});
}
function setTaskCompletedStyle(taskId = "", isCompleted = false) {
	if (taskId == "") {
		$(".ckb-completed").each(function (index) {
			if ($(this).val() == "1") {
				$(this).parent().addClass("task-completed");
			} else {
				$(this).parent().removeClass("task-completed");
			}
		});
	} else {
		var cardEle = $(`#is_completed${taskId}`).parent();
		if (isCompleted) {
			cardEle.addClass("task-completed");
		} else {
			cardEle.removeClass("task-completed");
		}
	}
}
