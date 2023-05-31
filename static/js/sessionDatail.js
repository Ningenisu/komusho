let MAXCNT = 1;
let SESSIONID = 0;
const sessionNaiyoInsert = () => {
	postSessionNaiyo()
}
const errorAlert = (text) => {
		alert(`エラーが発生しました。${text}`);
	};
const sessionNaiyoCreate = (items) => {
	if (MAXCNT <= items[0]) {
		MAXCNT = items[0] + 1;
	}
	const sessionMenuFluid = document.getElementById("sessionMenuFluid");
	const sessionNaiyo = document.getElementById("sessionNaiyo");
	const sessionNaiyoClone = sessionNaiyo.cloneNode(true);
	sessionNaiyoClone.style.display = "";
	sessionNaiyoClone.id = `sessionNaiyo${items[0]}`;

	const selectShumoku = sessionNaiyoClone.querySelector('[name="selectShumoku"]');
	selectShumoku.value = items[1];
	selectShumoku.setAttribute('remban', items[0]);

	const inputJuryo = sessionNaiyoClone.querySelector('[name="inputJuryo"]');
	inputJuryo.value = items[2];
	inputJuryo.setAttribute('remban', items[0]);

	const inputKaisu = sessionNaiyoClone.querySelector('[name="inputKaisu"]');
	inputKaisu.value = items[3];
	inputKaisu.setAttribute('remban', items[0]);

	const inputSetsu = sessionNaiyoClone.querySelector('[name="inputSetsu"]');
	inputSetsu.value = items[4];
	inputSetsu.setAttribute('remban', items[0]);

	const shumokuBiko = sessionNaiyoClone.querySelector('[name="shumokuBiko"]');
	shumokuBiko.value = items[5];
	shumokuBiko.setAttribute('remban', items[0]);

	const btnDelete = sessionNaiyoClone.querySelector('[name="btnDelete"]');
	btnDelete.setAttribute('remban', items[0]);
	sessionMenuFluid.appendChild(sessionNaiyoClone);
};
const initialize = () => {
	const path = location.pathname;
	const parts = path.split("/");
	SESSIONID = parts[2];
	let url = `/data/session/${SESSIONID}`;
	fetch(url)
	.then(response => response.json())
	.then(data => {
		const sessionMenuFluid = document.getElementById("sessionMenuFluid");
		sessionMenuFluid.innerHTML = "";
		data.forEach(items => {
			sessionNaiyoCreate(items);
		});
	});
};
window.onload = initialize;
const postSessionNaiyo = () => {
	let url = `/data/session/${SESSIONID}`;
	fetch(url, {
		method: "POST"
	}).then(response => response.json())
	.then(data => initialize())
	.catch(error => errorAlert(error.message));
};
const patchSession = (bodyList) => {
	let url = `/data/session/${SESSIONID}`;
	fetch(url, {
		method: "PATCH",
		headers: {
			"Content-Type": "application/json"
		},
		body: JSON.stringify(bodyList)
	}).then(response => response.json())
	.then(data => console.log(data))
	.catch(error => errorAlert(error.message));
};
const deleteSession = () => {
	let url = `/data/session/${SESSIONID}`;
	fetch(url, {
		method: "DELETE"
		// headers: {
		// 	"Content-Type": "application/json"
		// },
	}).then(response => response.json())
	.then(data => location.href = `/session`)
	.catch(error => errorAlert(error.message));
};
const patchSessionSub = (bodyList, remban) => {
	let url = `/data/session/${SESSIONID}/${remban}`;
	fetch(url, {
		method: "PATCH",
		headers: {
			"Content-Type": "application/json"
		},
		body: JSON.stringify(bodyList)
	}).then(response => response.json())
	.then(data => console.log(data))
	.catch(error => errorAlert(error.message));
};
const deleteSessionSub = () => {
	let url = `/data/session/${SESSIONID}/${remban}`;
	fetch(url, {
		method: "DELETE"
		// headers: {
		// 	"Content-Type": "application/json"
		// },
	}).then(response => response.json())
	.then(data => initialize())
	.catch(error => errorAlert(error.message));
};
window.addEventListener("load", () => {
	window.addEventListener("change", (event) => {
		if (event.target.hasAttribute("data-value1")) {
			dataSession = document.querySelectorAll('[data-value1]');
			
			bodyList = {};
			for (const elem of dataSession) {
				bodyList[elem.id] = elem.value;
			}
			patchSession(bodyList);
		}
		if (event.target.hasAttribute("data-value2")) {
			remban = event.target.getAttribute('remban');
			dataSession = document.querySelectorAll(`[data-value2][remban="${remban}"]`);
			// dataTextSession = document.querySelectorAll(`[data-text2][remban="${remban}"]`);
			
			bodyList = {};
			for (const elem of dataSession) {
				bodyList[elem.getAttribute('data-value2')] = elem.value;
			}
			patchSessionSub(bodyList, remban);
		}
	});
	window.addEventListener("click", (event) => {
		if (event.target.getAttribute('name') === "btnDelete") {
			remban = event.target.getAttribute('remban');
			deleteSessionSub(remban);
		}
	});
});

function proceed() {
	deleteSession();
}