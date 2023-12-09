const url = "https://file120.gofile.io/download/9e20a882-10e2-492a-b33a-edd4b4e04e7a/SteamWorld%20Build%20--%20fitgirl-repacks.site%20--.part1.rar";

const response = await fetch(url);

const fileName = response.headers.get("Content-Disposition");

const file = new File(fileName, await response.blob());

await file.write();

console.log("File downloaded successfully");