from Server.api import log, serverConfig, jdShopper, loginStatus

URL_TABLE = {
    "/log": log,
    "/config": serverConfig,
    "/jd-shopper": jdShopper,
    "/jd-login-status": loginStatus
}
