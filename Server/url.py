from Server.api import log, serverConfig, jdShopper, loginStatus, runningStatus, stopRunning, exitProcess

URL_TABLE = {
    "/log": log,
    "/config": serverConfig,
    "/jd-shopper": jdShopper,
    "/jd-login-status": loginStatus,
    "/jd-running-status": runningStatus,
    "/jd-stop-running": stopRunning,
    "/exit": exitProcess
}
