Cleaned up dndbeyond character dataset from [kaggle](https://www.kaggle.com/datasets/maximebonnin/dnd-characters-test)

1. Background, feats, inventory items and classes separated into classes themselves
2. For classes, a prediction of them being original or customized was made based on the name
3. Class has separate flags for the class itself and subclass
4. For classes and feats, a "setting" toggle was added, separating "Forgotten Realms" as default and adding 
(where possible) a speicifc setting. For unknown "None" is used
   1. For subclasses found in the wild on reddit or gmbinder, "market" was used as setting
5. For inventory items a rough estimation of the "base item" was made for some.
6. For inventory items, original name was lost in compression, at some point I'll restore it...
7. For inventory items, a gold value listed in the name was transfered into `value_gp` field
8. `date_modified` was transformed into a datetime object
9. For classes, an estimation of which subclass belongs to which class was made
   1. In the dataset itself it's all strings with no relation, so if there was an "Assassin" custom busclass 
   for Fighter class, it would've been missed
10. Race was normalized into a class as well, also specifying setting, UA, archived status and customization.
11. Where applicable, `__eq__` and `__hash__` were implemented, trying to make it easier to group into sets.
    1. For complex classes a class attribute `SEPARATE_ON_TAGS` were added to switch on and off distinction between 
    same named classes\feats and those customized\UA

For all classes, the same logic persists for those:
* `setting` "Forgotten Realms" for original, "market" for things found on the internet.
* `UA` marked True if specifically mentioned in the name or only exists in UA
* `archived` marked True if specifically mentioned in the name or only exists in archived (usually, archived UA)
* `customized` marked True as an estimation. **market things are not marked as such, unless speciifcally mentioned 
within the name. For those fully custom, `setting == None and customized == True` should be used**