const errorAlert = (text) => {
	alert(`エラーが発生しました。${text}`);
};
window.addEventListener("load", () => {
	const postAddKokyaku = (bodyList) => {
		let url = `/addkokyaku`;
		fetch(url, {
				method: "POST",
				headers: {
						"Content-Type": "application/json"
				},
				body: JSON.stringify(bodyList)
		}).then(response => response.json())
		.then(data => location.href = `/addkokyaku`)
		.catch(error => errorAlert(error.message));
	};
	const patchAddKokyakuData = (kokyakuId, bodyList) => {
		let url = `/addkokyaku/${kokyakuId}`;
		fetch(url, {
				method: "PATCH",
				headers: {
						"Content-Type": "application/json"
				},
				body: JSON.stringify(bodyList)
		}).then(response => response.json())
		.then(data => getAddKokyakuData(kokyakuId))
		.catch(error => errorAlert(error.message));
	};
	const getAddKokyakuData = (kokyakuId) => {
		
		let url = `/addkokyaku/${kokyakuId}`;
		fetch(url, {
				method: "GET",
				headers: {
						"Content-Type": "application/json"
				}
		}).then(response => response.json())
		.then(data => createKokyakuJoho(data))
		.catch(error => errorAlert(error.message));
	};

	const createKokyakuJoho = (kokyakuObj) => {
		const gender= document.querySelector(`input[name="gender"][value="${kokyakuObj[0]}"]`);
		gender.checked = true;
		const elemDataValue = document.querySelectorAll('[data-value]');
		let cnt = 1;
		elemDataValue.forEach((elem) => {
			elem.value = kokyakuObj[cnt];
			cnt += 1;
		});
	};

	const selectKokyaku = document.getElementById("selectKokyaku");
	const isOk = document.getElementById("isOk");
	isOk.addEventListener("click", () => {
		const bodyList = {};
		const elemDataValue = document.querySelectorAll('[data-value]');
		const inputGender = document.querySelector('input[name="gender"]:checked');

		elemDataValue.forEach((elem) => {
			bodyList[elem.id] = elem.value;
		});
		bodyList.gender = inputGender.value;
		const kokyakuId = selectKokyaku.value;
		if (kokyakuId === "") {
			postAddKokyaku(bodyList);
		} else {
			patchAddKokyakuData(kokyakuId, bodyList);
		}
	});
	selectKokyaku.addEventListener("change", (event) => {
		if (event.target.value === "") {
			location.href = `/addkokyaku`;
		} else {
			const kokyakuId = selectKokyaku.value;
			getAddKokyakuData(kokyakuId);
		}
	});
});