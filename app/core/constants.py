from string import Template


INVESTED_CANT_DELETE = 'В проект были внесены средства, не подлежит удалению!'
PROJECT_NAME_EXISTS = 'Проект с таким именем уже существует!'
PROJECT_NOT_FOUND = 'Проект не найден!'
NOT_PERMIT_CLOSED_PROJECT = 'Закрытый проект нельзя редактировать!'
NOT_PERMIT_FULL_AMOUNT_MORE_INVESTE_AMOUNT = 'При редактировании проекта  запрещено устанавливать требуемую сумму меньше внесённой.'
PASSWORD_LEN_MORE_THREE = 'Password should be at least 3 characters'
PASSWORD_CANT_CONTAINS_EMAIL = 'Password should not contain e-mail'
USER_REGISTERED = Template('Пользователь $user_email зарегистрирован.')
FULL_AMOUNT_SHOUL_BE_POSITIVE_INT = (
    'Требуемая сумма (full_amount)'
    ' проекта должна быть целочисленной'
    ' и больше 0.'
)
FULL_AMOUNT_SHOUL_BE_MORE_INVESTED_AMOUNT = (
    'Время начала бронирования '
    'не может быть больше времени окончания'
)
DELETE_USER_IS_NOT_PERMIT = 'Удаление пользователей запрещено!'
JWT_LIFETIME_SECONDS = 3600
MIN_LENGTH = 1
MAX_LENGTH = 100
