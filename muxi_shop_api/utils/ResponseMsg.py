from django.http import JsonResponse

from utils.BaseResponse import BaseResponse

# apps/goods/response.py
class GoodsResponse(BaseResponse):
    """商品模块响应类"""

    # DEFAULT_SUCCESS_MESSAGE = '操作成功'
    # DEFAULT_ERROR_MESSAGE = '操作失败'

    @classmethod
    def out_of_stock(cls, product_id: int) -> JsonResponse:
        """商品缺货响应"""
        return cls.error(
            message='商品缺货',
            code=409,
            data={'product_id': product_id, 'available': False}
        )

    @classmethod
    def price_updated(cls, old_price: float, new_price: float) -> JsonResponse:
        """价格更新响应"""
        return cls.success(
            message='价格更新成功',
            data={
                'old_price': old_price,
                'new_price': new_price,
                'change': new_price - old_price
            }
        )


# apps/user/response.py
class UserResponse(BaseResponse):
    """用户模块响应类"""

    DEFAULT_SUCCESS_MESSAGE = '用户操作成功'
    DEFAULT_ERROR_MESSAGE = '用户操作失败'

    @classmethod
    def login_success(cls, user_data: Dict, token: str) -> JsonResponse:
        """登录成功响应"""
        return cls.success(
            message='登录成功',
            data={
                'user': user_data,
                'token': token,
                'login_time': '2024-01-01 12:00:00'
            }
        )

    @classmethod
    def profile_updated(cls, updated_fields: List[str]) -> JsonResponse:
        """资料更新响应"""
        return cls.success(
            message='资料更新成功',
            data={'updated_fields': updated_fields}
        )

    @classmethod
    def unauthorized(cls, reason: str = None) -> JsonResponse:
        """未授权响应"""
        message = '未授权访问'
        if reason:
            message = f'{message}: {reason}'
        return cls.error(message=message, code=401)


# /apps/cart/response.py
class CartResponse(BaseResponse):
    """购物车模块响应类"""

    DEFAULT_SUCCESS_MESSAGE = '购物车操作成功'
    DEFAULT_ERROR_MESSAGE = '购物车操作失败'

    @classmethod
    def cart_empty(cls) -> JsonResponse:
        """购物车为空响应"""
        return cls.success(
            message='购物车为空',
            data={'item_count': 0, 'total_amount': 0}
        )

    @classmethod
    def item_added(cls, product_id: int, quantity: int, cart_total: int) -> JsonResponse:
        """商品添加响应"""
        return cls.success(
            message='商品已添加到购物车',
            data={
                'product_id': product_id,
                'quantity': quantity,
                'cart_total_items': cart_total
            }
        )

    @classmethod
    def insufficient_stock(cls, product_id: int, available: int, requested: int) -> JsonResponse:
        """库存不足响应"""
        return cls.error(
            message='库存不足',
            code=409,
            data={
                'product_id': product_id,
                'available_stock': available,
                'requested_quantity': requested
            }
        )


# apps/order/response.py
class OrderResponse(BaseResponse):
    """订单模块响应类"""

    DEFAULT_SUCCESS_MESSAGE = '订单操作成功'
    DEFAULT_ERROR_MESSAGE = '订单操作失败'

    @classmethod
    def order_created(cls, order_id: int, order_number: str) -> JsonResponse:
        """订单创建成功响应"""
        return cls.created(
            data={
                'order_id': order_id,
                'order_number': order_number,
                'status': 'pending'
            },
            message='订单创建成功'
        )

    @classmethod
    def payment_required(cls, order_id: int, amount: float) -> JsonResponse:
        """需要支付响应"""
        return cls.error(
            message='请完成支付',
            code=402,
            data={
                'order_id': order_id,
                'amount': amount,
                'payment_status': 'pending'
            }
        )