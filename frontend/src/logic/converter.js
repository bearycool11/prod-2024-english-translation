export default function convertPermissions(permission) {
  switch (permission) {
    case 'viewer':
      return 'Зритель'
    case 'reviewer':
      return 'Проверящий'
    case 'editor':
      return 'Редактор'
    case 'admin':
      return 'Администратор'
    case 'owner':
      return 'Владелец'
  }
}
