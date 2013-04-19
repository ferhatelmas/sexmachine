=========== 
Sex Machine
===========

This package uses the underlying data from the program "gender" by Jorg Michael (described `here <http://www.autohotkey.com/community/viewtopic.php?t=22000>`_).  Its use is pretty straightforward::

    >>> import sexmachine.detector as gender
    >>> d = gender.Detector()
    >>> d.get_gender(u"Bob")
    u'male'
    >>> d.get_gender(u"Sally")
    u'female'
    >>> d.get_gender(u"Pauley") # should be androgynous
    u'andy'

The result will be one of ``andy`` (androgynous), ``male``, ``female``, ``mostly_male``, or ``mostly_female``.  Any unknown names are considered andies. Moreover, you can set unknown value to whatever you want::
    
    >>> d = gender.Detector(unknown_value=u"ferhat")
    >>> d.get_gender(u"Pauley")
    u'ferhat'

I18N is fully supported::

    >>> d.get_gender(u"Álfrún")
    u'female'

Additionally, you can give preference to specific countries::

    >>> d.get_gender(u"Jamie")
    u'mostly_female'
    >>> d.get_gender(u"Jamie", u'great_britain')
    u'mostly_male'

Additionally, you can create a detector that is not case sensitive (default *is* to be case sensitive)::

    >>> d = sexmachine.detector.Detector(case_sensitive=False)
    >>> d.get_gender(u"sally")
    u'female'
    >>> d.get_gender(u"Sally")
    u'female'

Try to avoid creating many Detectors, as each creation means reading the data file.

Licenses
========

The generator code is distributed under the GPLv3.  The data file nam_dict.txt is released under the GNU Free Documentation License.