# utils/response.py
from django.http import JsonResponse
from typing import Any, Dict, List
from django.core.paginator import Paginator


class BaseResponse:
    """
    响应模板基类
    所有app的Response类都应该继承此类
    """

    # 类属性：默认配置
    DEFAULT_SUCCESS_CODE = 200
    DEFAULT_ERROR_CODE = 400
    DEFAULT_SUCCESS_MESSAGE = '操作成功'
    DEFAULT_ERROR_MESSAGE = '操作失败'

    @classmethod
    def success(
            cls,
            data: Any = None,
            message: str = None,
            code: int = None
    ) -> JsonResponse:
        """
        成功响应

        Args:
            data: 响应数据
            message: 成功消息，默认为类默认消息
            code: HTTP状态码，默认为类默认成功码

        Returns:
            JsonResponse: 标准化的JSON响应
        """
        response_data = {
            'code': code or cls.DEFAULT_SUCCESS_CODE,
            'message': message or cls.DEFAULT_SUCCESS_MESSAGE,
            'data': data,
            'success': True
        }
        return JsonResponse(response_data, status=response_data['code'])

    @classmethod
    def error(
            cls,
            message: str = None,
            code: int = None,
            details: Any = None,
            data: Any = None
    ) -> JsonResponse:
        """
        错误响应

        Args:
            message: 错误消息，默认为类默认错误消息
            code: HTTP错误码，默认为类默认错误码
            details: 错误详情（用于调试）
            data: 附加数据

        Returns:
            JsonResponse: 标准化的错误响应
        """
        response_data = {
            'code': code or cls.DEFAULT_ERROR_CODE,
            'message': message or cls.DEFAULT_ERROR_MESSAGE,
            'data': data,
            'success': False
        }

        # 仅在开发模式下显示错误详情
        from django.conf import settings
        if details and settings.DEBUG:
            response_data['details'] = details

        return JsonResponse(response_data, status=response_data['code'])

    @classmethod
    def paginate(
            cls,
            queryset,
            page: int = 1,
            page_size: int = 10,
            message: str = None,
            code: int = None,
            serializer=None
    ) -> JsonResponse:
        """
        分页数据响应

        Args:
            queryset: Django查询集
            page: 当前页码
            page_size: 每页大小
            message: 响应消息
            code: HTTP状态码
            serializer: 可选的序列化器函数

        Returns:
            JsonResponse: 分页格式的响应
        """
        paginator = Paginator(queryset, page_size)
        page_obj = paginator.get_page(page)

        if serializer:
            items = serializer(page_obj.object_list, many=True).data
        else:
            items = list(page_obj.object_list.values())

        pagination_data = {
            'items': items,
            'pagination': {
                'current_page': page_obj.number,
                'page_size': page_size,
                'total_items': paginator.count,
                'total_pages': paginator.num_pages,
                'has_next': page_obj.has_next(),
                'has_previous': page_obj.has_previous(),
            }
        }

        return cls.success(
            data=pagination_data,
            message=message or '分页数据获取成功',
            code=code
        )

    @classmethod
    def created(cls, data: Any = None, message: str = None) -> JsonResponse:
        """资源创建成功响应"""
        return cls.success(data=data, message=message or '创建成功', code=201)

    @classmethod
    def not_found(cls, message: str = None, details: Any = None) -> JsonResponse:
        """资源未找到响应"""
        return cls.error(
            message=message or '资源未找到',
            code=404,
            details=details
        )

    @classmethod
    def validation_error(
            cls,
            errors: Dict[str, List[str]],
            message: str = None
    ) -> JsonResponse:
        """参数验证错误响应"""
        return cls.error(
            message=message or '参数验证失败',
            code=422,
            data={'errors': errors}
        )

    @classmethod
    def custom_response(
            cls,
            success: bool,
            data: Any = None,
            message: str = None,
            code: int = None,
            **kwargs
    ) -> JsonResponse:
        """
        自定义响应，可以添加额外字段

        Args:
            success: 是否成功
            data: 响应数据
            message: 消息
            code: 状态码
            **kwargs: 额外字段

        Returns:
            JsonResponse: 自定义响应
        """
        base_response = {
            'code': code or (cls.DEFAULT_SUCCESS_CODE if success else cls.DEFAULT_ERROR_CODE),
            'message': message or (cls.DEFAULT_SUCCESS_MESSAGE if success else cls.DEFAULT_ERROR_MESSAGE),
            'data': data,
            'success': success
        }
        base_response.update(kwargs)

        return JsonResponse(base_response, status=base_response['code'])