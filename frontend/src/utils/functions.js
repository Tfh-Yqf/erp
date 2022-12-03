export function removeItem(items, item) {
  let index = [...items].findIndex(_item => _item.id == item.id);
  if (index != -1) {
    items.splice(index, 1);
  }
  return items
}

export function removeItemM(items, item) {
  let index = [...items].findIndex(_item => _item.material == item.material);
  if (index != -1) {
    items.splice(index, 1);
  }
  return items
}

export function replaceItem(items, item) {
  let index = [...items].findIndex(_item => _item.id == item.id);
  if (index != -1) {
    items.splice(index, 1, item);
  }
  return items
}

export function insertItem(items, item) {
  let index = [...items].findIndex(_item => _item.id == item.id);
  if (index == -1) {
    items.splice(0, 0, item);
  }
  return items
}

export function insertItemM(items, item) {
  let index = [...items].findIndex(_item => _item.material == item.material);
  if (index == -1) {
    items.splice(0, 0, item);
  }
  return items
}

export function removeItemBatch(items, item) {
  let index = [...items].findIndex(_item => _item.key == item.key);
  if (index != -1) {
    items.splice(index, 1);
  }
  return items
}

export default { removeItem, removeItemM,  replaceItem, insertItem, insertItemM, removeItemBatch }