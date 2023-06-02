$(document).ready(function () {
	setTaskCompletedStyle();
	$(".ckb-completed").click(function (e) {
		e.preventDefault();
		var isCompleted = $(this).prop("checked");
		var taskId = $(this).attr("data-task-id");
		setCompleteStatus(taskId, isCompleted);
	});
	$(".btn-del-task").click(function (e) {
		e.preventDefault();
		var taskId = $(this).attr("data-task-id");
		showModalConfirm(
			"exampleModal",
			"Do you want to delete this task?",
			taskId
		);
		// delTask(taskId);
	});
});
function setCompleteStatus(taskId, isCompleted) {
	var url = "/set_complete";
	var data = {
		task_id: taskId,
		is_completed: isCompleted
	};
	const callBackFunc = function (response) {
		if (response.status == "true") {
			$(`#is_completed${taskId}`).prop("checked", response.is_completed);
			setTaskCompletedStyle(taskId, response.is_completed);
			toastMessage(response.message, response.status);
		} else {
			toastMessage(response.message, response.status);
		}
	};
	callAjaxPostRequest(url, data, callBackFunc);
}
function setTaskCompletedStyle(taskId = "", isCompleted = false) {
	if (taskId == "") {
		$(".ckb-completed").each(function (index) {
			let itemNumber = $(this).attr("data-task-id");
			if ($(this).val() == "1") {
				$(`.is_completed${itemNumber}`).addClass("task-completed");
			} else {
				$(`.is_completed${itemNumber}`).removeClass("task-completed");
			}
		});
	} else {
		var cardEle = $(`.is_completed${taskId}`);
		if (isCompleted) {
			cardEle.addClass("task-completed");
		} else {
			cardEle.removeClass("task-completed");
		}
	}
}

function delTask(taskId) {
	var url = "/delete_task";
	var data = {
		task_id: taskId
	};
	const callBackFunc = function (response) {
		if ((response.status = "true")) {
			$(`#task-item-${taskId}`).remove();
		}
		toastMessage(response.message, response.status);
	};
	callAjaxPostRequest(url, data, callBackFunc);
}

function toastMessage(message, status) {
	const toastLiveEle = $("#liveToast");
	$(".toast-body").text(message);
	toastLiveEle.removeClass("bg-success");
	toastLiveEle.removeClass("bg-error");
	if (status == "true") {
		toastLiveEle.addClass("bg-success");
	} else {
		toastLiveEle.addClass("bg-error");
	}
	const toastBootstrap = bootstrap.Toast.getOrCreateInstance(toastLiveEle);
	toastBootstrap.show();
}

function showModalConfirm(modalId, message, taskId) {
	$(`#${modalId}`).modal("show");
	$(".modal-body").text(message);
	$("#btn-accept").click(function (e) {
		e.preventDefault();
		delTask(taskId);
		$(`#${modalId}`).modal("hide");
	});
}

function callAjaxPostRequest(url, data, callBackFunc) {
	$.ajax({
		url: url,
		method: "POST",
		contentType: "application/json",
		data: JSON.stringify(data),
		dataType: "json",
		success: function (response) {
			console.log(response);
			callBackFunc(response);
		},
		error: function (e) {
			console.log(e);
		}
	});
}
