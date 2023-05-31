
const errorAlert = (text) => {
	alert(`エラーが発生しました。${text}`);
};
window.addEventListener("load", () => {
		const search = document.getElementById("search");
		const selectKokyaku = document.getElementById("selectKokyaku");
		const sessionAt1 = document.getElementById("sessionAt1");
		const sessionAt2 = document.getElementById("sessionAt2");
		const dataList = document.getElementById("dataList");
		const addSession = document.getElementById("addSession")

		const today = new Date();
		const oneYearAgo = new Date(today.getFullYear() - 1, today.getMonth(), today.getDate());

		const year = oneYearAgo.getFullYear();
		const month = String(oneYearAgo.getMonth() + 1).padStart(2, '0');
		const day = String(oneYearAgo.getDate()).padStart(2, '0');

		const dateString = `${year}-${month}-${day}`;
		sessionAt1.value = dateString
		search.addEventListener("click", () => {
				let url = "/data/session"
				url += `?id=${selectKokyaku.value}`
				if (sessionAt1.value) {
						url += `&sessionAt1=${sessionAt1.value}`
				}
				if (sessionAt2.value) {
						url += `&sessionAt2=${sessionAt2.value}`
				}
				fetch(url)
				.then(response => response.json())
				.then(data => {
						dataList.innerHTML = "";
						data.forEach(items => {
								const trItem = document.createElement('tr');
								let cnt = 1;
								for (const elem of items) {
										const tdItem = document.createElement('td');
										if (cnt === 4) {
												tdItem.innerHTML = `<button type="button" onclick="location.href='/session/${elem}'" class="btn btn-secondary" cntno=${elem}>詳細</button>`;
										} else {
												tdItem.innerText = elem
										}
										trItem.appendChild(tdItem);
										cnt += 1;
								}
								dataList.appendChild(trItem);
						});
				});
		});
		const postSession = (bodyList) => {
				let url = `/data/session`;
				fetch(url, {
						method: "POST",
						headers: {
								"Content-Type": "application/json"
						},
						body: JSON.stringify(bodyList)
				}).then(response => response.json())
				.then(data => location.href = `/session/${data[0]}`)
				.catch(error => errorAlert(error.message));
		};
		addSession.addEventListener("click", () => {
				bodyList = {"kokyakuId": selectKokyaku.value}
				postSession(bodyList);
		});
});