
def user_role(request):
    """
    Context processor que añade 'user_role' al contexto de todas las plantillas.
    Si el usuario no está autenticado o no tiene perfil, devuelve None.
    """
    user = request.user
    role = None
    if user.is_authenticated:
        # Intentamos leer user.userprofile, pero si no existe, lo ignoramos
        profile = getattr(user, 'userprofile', None)
        if profile is not None:
            role = profile.role
    return {'user_role': role}