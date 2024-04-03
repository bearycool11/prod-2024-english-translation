export default function convertStatuses(permission) {
  switch (permission) {
    case 'WAITING':
      return 'ОЖИДАЕТ'
    case 'REJECTED':
      return 'ОТКЛОНЁН'
    case 'APPROVED':
      return 'ПОДТВЕРЖДЕН'
    case 'OPEN':
      return 'ОТКРЫТ'
    case 'NOT_READY':
      return 'НЕ ОТЛОЖЕН'
    case 'SENT_OK':
      return 'ОТПРАВЛЕН'
  }
}
