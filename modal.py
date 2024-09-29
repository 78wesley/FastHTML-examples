from fasthtml.common import *

db = database("modal_sqlite.db")
servers = db.t.servers
users = db.t.users
if servers not in db.t:
    users.create(dict(fqdn=str), pk="fqdn")
    servers.create(id=int, fqdn=str, pk="id")

Server = servers.dataclass()
User = users.dataclass()
app = FastHTMLWithLiveReload(hdrs=(picolink))


@patch
def __ft__(self: Server):
    return Li(
        *self.fqdn,
        id=f"server-{self.id}",
        hx_delete=f"/server/{self.id}",
        hx_target="this",
        hx_swap="outerHTML",
    )


@app.get("/")
def home():
    return (
        Title("Server Management"),
        Main(
            H1("Manage Servers"),
            P(
                B("modal_js: "),
                "This has been made without a form tag. It uses hx_vals to get the value of the input field and it does have a footer tag. ",
                A(
                    "Security Considerations",
                    href="https://github.com/picocss/pico/issues/616",
                ),
            ),
            P(
                B("modal_form: "),
                "This has been made with a form tag. Without a footer tag because Pico CSS doesn't like a form tag after a article tag. ",
                A("GitHub issue", href="https://github.com/picocss/pico/issues/616"),
            ),
            P(
                "Both modals can't be closed by clicking outside the modal and they can't be closed by pressing the escape key. "
            ),
            Div(
                Button(
                    "modal_form",
                    hx_get="/modal_form",
                    hx_target="#server-list",
                    hx_swap="beforeend",
                ),
                Button(
                    "modal_js",
                    hx_get="/modal_js",
                    hx_target="#server-list",
                    hx_swap="beforeend",
                ),
                cls="grid",
            ),
            cls="container",
        ),
        Div(
            H5("Servers list:"),
            *servers(order_by="id"),
            cls="container",
            id="server-list",
        ),
    )


@app.get("/modal_form")
def modal_form():
    return Dialog(
        Article(
            Header(
                Button(
                    aria_label="Close",
                    rel="prev",
                    hx_get="/close-modal",
                    hx_target="#modal_form",
                    hx_swap="outerHTML",
                ),
                H2(Strong("Add server")),
            ),
            Form(
                Label("FQDN:", _for="fqdn"),
                Input(
                    type="text",
                    name="fqdn",
                    id="fqdn",
                    placeholder="Enter FQDN",
                    required=True,
                ),
                Div(
                    Button(
                        "Cancel",
                        type="button",
                        hx_get="/close-modal",
                        hx_target="#modal_form",
                        hx_swap="outerHTML",
                        cls="secondary",
                    ),
                    Button(
                        "Add",
                        type="submit",
                        hx_target="#modal_form",
                        hx_post="/add-server",
                        hx_swap="outerHTML",
                    ),
                    cls="grid",
                ),
            ),
        ),
        id="modal_form",
        open=True,
    )


@app.get("/modal_js")
def modal_js():
    return DialogX(
        Header(
            Button(
                aria_label="Close",
                rel="prev",
                hx_get="/close-modal",
                hx_target="#modal_js",
                hx_swap="outerHTML",
            ),
            H2("Add Server"),
        ),
        Label("FQDN:", _for="fqdn"),
        Input(
            type="text", name="fqdn", id="fqdn", placeholder="Enter FQDN", required=True
        ),
        Footer(
            Button(
                "Cancel",
                type="button",
                hx_get="/close-modal",
                hx_target="#modal_js",
                hx_swap="outerHTML",
                cls="secondary",
            ),
            Button(
                "Add",
                type="submit",
                hx_post="/add-server",
                hx_target="#modal_js",
                hx_swap="outerHTML",
                hx_vals="js:{fqdn: document.getElementById('fqdn').value}",
            ),
            cls="grid",
        ),
        id="modal_js",
        open=True,
    )


@app.get("/close-modal")
def close_modal():
    return ""


@app.post("/add-server")
def add_server(fqdn: str):
    return servers.insert(Server(fqdn=fqdn))


@app.delete("/server/{id}")
def delete_server(id: int):
    servers.delete(id)
    return ""


serve()
