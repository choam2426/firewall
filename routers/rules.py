from fastapi import APIRouter, Path, Request
from fastapi.templating import Jinja2Templates

from src.db_connect import mongodb
from src.iptables_command import *
from src.update_iptables_rules_to_db import rewrite

from .schemas import iptable_rule

router = APIRouter(prefix="/rules")
templates = Jinja2Templates(directory="templates")


@router.get(path="/")
async def get_rules_page(request: Request):
    await rewrite()
    iptable_rules_collection = mongodb.db["iptables_rules"]
    rules = await iptable_rules_collection.find({}).to_list(None)
    return templates.TemplateResponse(
        request=request, name="rules.html", context={"rules": rules}
    )


@router.get(path="/create")
async def get_rule_create_page(request: Request):
    return templates.TemplateResponse(request=request, name="rule_form.html")


@router.post(path="/create")
async def create_iptables_rules(request: Request, new_rule_data: iptable_rule):
    print(append_iptables_rule(new_rule_data.model_dump()))
    await rewrite()
    return 1


@router.get(path="/update/{rule_number}")
async def get_rule_update_page(request: Request):
    return templates.TemplateResponse(request=request, name="update_rule_form.html")


@router.put(path="/update/{rule_number}")
async def update_iptables_rules(
    request: Request, new_rule_data: iptable_rule, rule_number: int = Path()
):
    iptables_rules_collection = mongodb.db["iptables_rules"]
    iptables_rule_number = await iptables_rules_collection.find_one(
        {"number": rule_number}, {"_id": 0, "real_num": 1}
    )
    new_rule_data = new_rule_data.model_dump()
    print(iptables_rule_number)
    return 1


@router.delete(path="/{rule_number}")
async def get_rule_create_page(request: Request, rule_number: int = Path()):
    print(rule_number)
    return 1
