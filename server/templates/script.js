const delay = ms => new Promise(res => setTimeout(res, ms));
var abort;

function set_abort() {
    abort = true;
}

async function start_tracking() {
    abort = false

    while (true) {
        console.log("checking song")
        if (abort)
            break

        document.getElementById("track_form").submit();
        await delay(5000);
    }
}
