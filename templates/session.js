

// import "./module/_header.js";
// import "./module/_footer.js";
// import * as dialog from "tms_client/dialog";
// import * as webTools from "tms_client/webTools";
// import * as tmsFetch from "tms_client/tmsFetch";
// import * as commons from "./module/_commons.js";
// import * as serverOutput from "./module/_serverOutput.js";

let RESULT = {};

/**
 * 架電実施率
 * WEBAPI呼び出し（GET:/v1/jisshiritsu）
 * @function
 * @returns {Promise} 取得結果
 */
const getjisshiritsuFollowListAsync = async(ym) => {
	const params = new URLSearchParams();
	const url = webTools.makeURL(`/v1/jisshiritsu/follow/${ym}/list`);
	url.search = params.toString();
	console.log(url.toString());
	const result = await tmsFetch.json(url.toString(), {
		"method": "GET"
	});
	return result;
};

const getjisshiritsuFollowList = async(ym) => {
	let result = {};
	try {
		result = await getjisshiritsuFollowListAsync(ym);
	} catch (err) {
		await dialog.alertAsync(err.message);
	}
	return result;
};


window.addEventListener("load", () => {
	const search = document.getElementById("search");
	const selectKokyaku = document.getElementById("selectKokyaku");
	search.addEventListener("click", () => {
		kokyakuData(searchParam);
		let url = "/data/kokyaku"
		url += `?id=${selectKokyaku.value}`
		fetch(url)
        .then(response => response.json())
        .then(data => {
          console.log(data);
        });
	});
});

window.onload = initialize;
