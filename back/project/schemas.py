from pydantic import BaseModel
from typing import Union, List

class ValidationError(BaseModel):
    loc: List[Union[str, int]]
    msg: str
    type: str

class HTTPValidationError(BaseModel):
    detail: list[ValidationError]


class OAuth2PasswordRequestFormSchema(BaseModel):
    username: str
    password: str
    grant_type: str = "password"
    scope: str = ""
    client_id: str = ""
    client_secret: str = ""


class Token(BaseModel):
    access_token: str
    token_type: str
    message: str
    user_id: int
    user_email: str
    fullname: str
    account: str
    result: bool

class Message(BaseModel):
    message: str
    result: bool

class UserSchema(BaseModel):
    nickname: str
    fullname: str
    email: str
    password: str | None = None


class AccountUserSchema(BaseModel):
    account: object
    user: object

class RolesSchema(BaseModel):
    name: str


class AccountSchema(BaseModel):
    name: str


class AccountsModulesSchema(BaseModel):
    module_id: int
    account_id: int


class PermissionsSchema(BaseModel):
    name: str
    description: str


class SysUserPermissionsSchema(BaseModel):
    user_id: int
    permission_submenu_id: int

class ModulesSchema(BaseModel):
    name: str


class ModulesPermissionsSchema(BaseModel):
    module_id: int
    permission_id: int


class SysMenusSchema(BaseModel):
    name: str
    order: int | str


class SysSubMenusSchema(BaseModel):
    name: str
    menu_id: int
    link: str
    icon: str
    order: int

class SysNichosSchema(BaseModel):
    name: str


class SysAccountsNichosSchema (BaseModel):
    account_id: int
    nicho_id: int


class SysNichosMenusSchema(BaseModel):
    nicho_id: int
    menu_id: int

class SysAccountsSubmenusSchema(BaseModel):
    submenu_id: int
    account_id: int

class SysPermissionsSubmenusSchema(BaseModel):
    permission_id: int
    submenu_id: int


class CustomersCategoriesSchema(BaseModel):
    start_date: str
    full_name: str
    company_name: str
    status: bool
    email: str
    phone: str
    type_customer_id: int
    default: bool

class CategoriesCatalogoSchema(BaseModel):
    code: str
    name: str
    type_category_id: int


class TypeCategoriesCatalogoSchema(BaseModel):
    code: str
    name: str


class SubCategoriesSchema(BaseModel):
    code: str
    name: str
    category_id: int


class BranchesSchema(BaseModel):
    code: str
    name: str 
    street: str
    interior_number: str
    exterior_number: str
    between_street: str
    locality_id: int


class StatesSchema(BaseModel):
    name: str


class LocalitiesSchema(BaseModel):
    name: str
    cp: str
    municipality_id: int


class SuppliersSchema(BaseModel):
    company_name: str
    trade_name: str
    status: bool
    email: str
    contact_name: str
    phone: str
    cell_phone: str
    rfc: str
    currency_id: int
    street: str
    interior_number: str
    exterior_number: str
    locality_id: int

class CurrencySchema(BaseModel):
    code: str
    name: str


class StoreSchema(BaseModel):
    code: str
    name: str
    branch_id: int
    street: str
    interior_number: str
    exterior_number: str
    between_street: str
    locality_id: int
    default: bool


class UnitsSchema(BaseModel):
    code: str
    name: str
    value:float


class LineSchema(BaseModel):
    code: str
    name: str
    has_merma: bool
    category_id: int


class BrandSchema(BaseModel):
    code: str
    name: str


class ArticlesSchema(BaseModel):
    code: str
    name: str
    weight: float
    bar_code: str
    line_id: int
    unit_id: int
    brand_id: int
    iva_id: int
    ieps_id: int

class CtgArticlesPriceSchema(BaseModel):
    price_type: str | None
    article_id: int
    price: float
    default: bool

class CustomersTypeSchema(BaseModel):
    code: str
    name: str


class InvMovementsTypeSchema(BaseModel):
    name: str


class InvMovementsSchema(BaseModel):
    type_movement_id: int
    date: str
    store_id: int
    status_movement_id: int
    destination_store_id: int | None


class InvMovementsDetailsSchema(BaseModel):
    movement_id: int
    article_id: int
    quantity: float
    cost: float | None
    presentation_id: int | None
    real_quantity_equivalent: float | None

class InvStockSchema(BaseModel):
    store_id: int
    article_id: int
    stock: float

class PurOrdersSchema(BaseModel):
    supplier_id: int
    store_id: int
    status_order_id: int
    reference: str

class PurOrdersOptionsIVASchema(BaseModel):
    porcentaje: float
    descripcion: str
    activo: bool

class CtgIepschema(BaseModel):
    porcentaje: float
    descripcion: str
    activo: bool

class PurOrdersDetailschema(BaseModel):
    article_id: int
    quantity: float
    iva_id: int
    price: float
    comments: str
    order_id: int
    real_quantity_equivalent: float | None
    presentation_id: int | None

class PurReceiptsSchema(BaseModel):
    order_id: int | None
    date: str | None
    hour: str | None
    execute: int | None
    movement_id: int | None

class PurReceiptsExecuteSchema(BaseModel):
    execute: bool | None

class PurReceivedDetailsSchema(BaseModel):
    receipt_id: int
    detail_id: int
    quantity: float
    comments: str | None


class CtgStoreCountersShema(BaseModel):
    name: str
    branch_id: int
    default: bool

class SlsSalesShema(BaseModel):
    sales_status_id: int
    sales_type_id: int
    store_id: int
    cliente_id: int
    store_counters_id: int
    table_id: int | None
    reference: str | None
    user_id: int

class SlsSalesDetailsShema(BaseModel):
    sale_id: int
    article_id: int
    quantity: float
    unit_price: float
    discount: float
    subtotal: float
    tax: float
    observations: str | None

class SlsSalesDetailsQuantityShema(BaseModel):
    quantity: float


class CtgPresentationTypeShema(BaseModel):
    name: str


class CtgArticlePresentationshema(BaseModel):
    article_id: int
    type_presentation_id: int
    quantity_equivalent: float
    price: float